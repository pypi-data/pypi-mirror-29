import requests
from bs4 import BeautifulSoup
import re
import pprint
from operator import attrgetter
import youtube_dl
import tempfile
import pathlib
import shutil
import os


from .scraper import ScrapingError


YOUTUBE_BAD_SELECTOR_MESSAGE = "Doesn't work anymore possibly because YouTube changed their layout"


class YouTubeScrapingError(ScrapingError):
    def __init__(self, message=YOUTUBE_BAD_SELECTOR_MESSAGE):
        self.message = message


def is_string_duration(s):
    return re.match(r'^\d{1,2}(?:\:\d{2})+$', s) is not None


def parse_string_duration(s):
    """Converts a string time duration to seconds; e.g., 1:03 -> 63 or 2:51 -> 171"""
    ret = 0
    if not is_string_duration(s):
        # raise YouTubeScrapingError
        raise ValueError('%s is not a valid time string; needs e.g., 12:03' % s)
    for i, n in enumerate(reversed([int(x) for x in s.split(':')])):
        ret += 60**i * n
    return ret


class YouTubeSearchResult:
    def __init__(self, token, duration, rank, title, artist):
        self.token = token
        self.duration = duration
        self.rank = rank
        self.title = title
        self.artist = artist


    def dl(self, output_directory='.', quiet=True):
        filename = '%s - %s' % (self.artist, self.title)
        # First save to tmp and later copy to desired output directory
        qualified_filename = os.path.join(tempfile.gettempdir(), filename)
        ytdl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '0'
            }],
            'outtmpl': qualified_filename + '.%(ext)s',
            'quiet': quiet
        }
        with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
            ytdl.download(['https://youtube.com/watch?v=' + self.token])
        # Move completed file to output directory
        dst_filename = shutil.move(qualified_filename + '.mp3', output_directory)
        return dst_filename



class YouTubeSearch:
    def __init__(self, artist, song_title):
        query = artist + ' ' + song_title
        r = requests.get('https://www.youtube.com/results',
                         params = {'search_query': query})
        s = BeautifulSoup(r.text, 'html.parser')
        self.results = {}
        link_test = re.compile(r'watch\?v=([A-Za-z0-9\_-]+)$')
        rank = 1
        for link in s.find_all(lambda x: x.has_attr('title') and x.has_attr('href') and link_test.search(x.get('href'))):
            token = link_test.search(link.get('href')).group(1)
            if token is None or token in self.results:
                continue
            video_title = link.get('title')

            # Find duration of video
            li = link.find_parent('li')
            if li is None:
                raise YouTubeScrapingError
            video_time = li.find(class_='video-time')
            if video_time is None:
                raise YouTubeScrapingError
            duration = parse_string_duration(video_time.get_text())

            # Record this result
            self.results[token] = YouTubeSearchResult(token=token,
                                                      rank=rank,
                                                      duration=duration,
                                                      title=song_title,
                                                      artist=artist)
            rank += 1
        del r



    def get_ordered_results(self):
        return sorted((result for _, result in self.results.items()), key=attrgetter('rank'))


    def most_likely_result(self, ground_truth_duration):
        """Naively tries to find the most likely match based on actual duration of the song from an authoritative source"""
        return min((result for _, result in self.results.items()), key=lambda x: x.rank*max(1, abs(ground_truth_duration - x.duration))) # +/- 1 second difference is the same as 0 difference





# a = YouTubeSearch('rihanna calvin harris this is what you came for')
# pprint.pprint([{'rank': x.rank, 'token': x.token, 'title': x.title, 'duration': x.duration} for x in a.get_ordered_results()])
# prediction = a.most_likely_result(ground_truth_duration=222)
# print('\nMost likely: rank=%s, token=%s, title=%s, duration=%s\n' % (prediction.rank, prediction.token, prediction.title, prediction.duration))
