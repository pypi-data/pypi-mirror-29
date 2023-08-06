import discogs_client
import datetime
import re
from operator import attrgetter
from mutagen.id3 import ID3, APIC, TPE1, TIT2, TRCK, TALB, TPUB, TCON, TYER, TDOR, TDRL, TDTG
import requests
from itertools import islice


from .yt import is_string_duration


def clean_string(s):
    s = re.sub(r'[\[\]\{\}\(\)\.!;,\?]', '', s)
    s = re.sub(r'\-', ' ', s)
    return s.lower()


class DiscogsEntry:
    def __init__(self, master, track):
        self.master = master
        self.track = track


    def get_artists(self):
        artists = list(map(attrgetter('name'), self.master.main_release.artists))
        if hasattr(self.track, 'extraartists'):
            extra = set(map(attrgetter('name'), self.track.extraartists))
            artists.extend(extra.difference(artists))
        return artists


    def get_release_title(self):
        return self.master.title


    def get_genres(self):
        return self.master.genres


    def get_labels(self):
        return map(attrgetter('name'), self.master.main_release.labels)


    # def get_released_date(self):
    #     """Returns the date when the music was originally released apparently in yyyy-MM-dd format"""
    #     return self.master.main_release.released if hasattr(self.master.main_release, 'released') else ''


    def get_year(self):
        return str(self.master.main_release.year)


    def get_album_art_url(self):
        return self.master.main_release.images[0]['resource_url'] if len(self.master.main_release.images) > 0 else None


    def __str__(self):
        artists = ', '.join(self.get_artists())
        return '%s - %s - %s (%s) -- %s' % (artists, self.get_release_title(), self.track.title, self.get_year(), self.track.duration)


    def to_id3_tags(self, audio_path):
        """Loads an MP3 file and adds ID3v2.4 tags based on the given discogs entry"""
        audio = ID3(audio_path, v2_version=4)

        # Set album art
        album_art_url = self.get_album_art_url()
        if album_art_url:
            r = requests.get(album_art_url)
            audio.add(APIC(
                encoding=3,
                mime='image/jpeg',
                type=3,
                desc='Cover',
                data=r.content
            ))
            del r

        # Set title
        audio.add(TIT2(encoding=3, text=[self.track.title]))

        # Set artists
        audio.add(TPE1(encoding=3, text=self.get_artists()))

        # Set album
        audio.add(TALB(encoding=3, text=[self.get_release_title()]))

        # Set track number
        audio.add(TRCK(encoding=3, text=[self.track.position]))

        # Set labels
        labels = list(self.get_labels())
        if len(labels) > 0:
            audio.add(TPUB(encoding=3, text=labels[0:1]))

        # Set genres
        audio.add(TCON(encoding=3, text=self.get_genres()))

        # Set year
        audio.add(TYER(encoding=3, text=[self.get_year()])) # for backwards compatibility with v2.3
        # The timestamp fields are based on a subset of ISO 8601. When being as
        # precise as possible the format of a time string is
        # yyyy-MM-ddTHH:mm:ss (year, "-", month, "-", day, "T", hour (out of
        # 24), ":", minutes, ":", seconds), but the precision may be reduced by
        # removing as many time indicators as wanted. Hence valid timestamps
        # are
        # yyyy, yyyy-MM, yyyy-MM-dd, yyyy-MM-ddTHH, yyyy-MM-ddTHH:mm and
        # yyyy-MM-ddTHH:mm:ss. All time stamps are UTC. For durations, use
        # the slash character as described in 8601, and for multiple non-
        # contiguous dates, use multiple strings, if allowed by the frame
        # definition.
        audio.add(TDRL(encoding=3, text=[self.get_year()]))
        audio.add(TDOR(encoding=3, text=[self.get_year()]))

        # Set tagging time
        # aka right now
        # for completeness sake
        audio.add(TDTG(encoding=3, text=[datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M')]))

        # Write to disk
        audio.save()


class DiscogsSearcher:
    def __init__(self, user_token):
        self.client = discogs_client.Client('orangewire/0.1', user_token=user_token)


    def by_track(self, track_name, min_words_in_common=0.7, limit=20, **kwargs):
        ret = []

        kwargs['type'] = 'master'
        kwargs['track'] = track_name
        # kwargs implicitly includes 'artist' etc.

        # Start search
        r = self.client.search(**kwargs)

        # Find relevant tracks in each result's tracklist
        # For some reason discogs allows searching by track name but
        # only can provide a list of track names as each search result
        queryv = set(clean_string(track_name).split(' '))
        for master in islice(r, limit):
            for track in master.tracklist:
                if len(track.duration) == 0:
                    # it's useless without duration
                    continue
                titlev = set(clean_string(track.title).split(' '))
                # Naively find the match by comparing words. Works
                # because discog's search engine doesn't seem
                # that advanced.
                score = len(set.intersection(queryv, titlev))/min(len(titlev), len(queryv))
                if score >= min_words_in_common:
                    entry = DiscogsEntry(master=master, track=track)
                    ret.append(entry)

        return ret


    def by_album(self, album_name, limit=30, **kwargs):
        ret = []

        kwargs['type'] = 'master'
        kwargs['release_title'] = album_name
        # kwargs implicitly includes 'artist' etc.

        # Start search
        r = self.client.search(**kwargs)
        # Filter down to those where each track has a duration
        for master in islice(r, limit):
            if all(is_string_duration(track.duration) for track in master.tracklist):
                ret.append(master)
        return ret


def entries_from_master(master):
    ret = []
    for track in master.tracklist:
        ret.append(DiscogsEntry(master=master, track=track))
    return ret
