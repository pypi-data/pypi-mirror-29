#!/usr/bin/env python3

import discogs_client
import argparse
import sys
from operator import attrgetter
import pathlib


from .yt import *
from .discogs import *


def parse_int(s):
    try:
        return int(s)
    except ValueError:
        return None


def main():
    parser = argparse.ArgumentParser(prog='orangewire',
                                     description='Download music from YouTube with proper tagging')
    parser.add_argument('--track-name', required=False, help='Search by track name. Must use either this or --album-name')
    parser.add_argument('--album-name', required=False, help='Search by album name. Must use either this or --track-name')
    parser.add_argument('--artist-name', required=False, default='', help='Searches by artist name')
    parser.add_argument('--discogs-token', required=False, help='User token from your Discogs account https://www.discogs.com/settings/developers')
    parser.add_argument('--output-directory', required=False, default='.', help='Where you want the mp3 files to be saved to; defaults to .')
    parser.add_argument('--verbose', required=False, action='store_true')
    args = vars(parser.parse_args())

    # First try to find discogs user token
    config_filepath = pathlib.Path.home().joinpath('.orangewire')
    # Your config file is ~/.orangewire and all that should be in it is your user token on the first line
    # You can get a user token by registering an account at Discogs.com and going to https://www.discogs.com/settings/developers
    if args.get('discogs_token'):
        user_token = args.get('discogs_token')
    elif config_filepath.exists():
        with config_filepath.open() as f:
            user_token = f.readline().strip()
    else:
        print('You need to either supply a discogs.com user token with --discogs-token or have a file at ~/.orangewire containing this user token. To get one, make a discogs.com account and go to https://www.discogs.com/settings/developers')
        sys.exit(1)

    # Make sure output_directory works
    output_directory_path = pathlib.Path(args['output_directory'])
    if not output_directory_path.exists() or not output_directory_path.is_dir():
        print('Supplied --output-directory (%s) is invalid' % args['output_directory'])
        sys.exit(1)

    yt_dl_queue = []
    if args['verbose']:
        print('-----\nSearching discogs.com…')
    d = DiscogsSearcher(user_token=user_token)
    if args.get('track_name') is not None and args.get('album_name') is not None:
        print('You can only either search by --track-name or --album-name but not both')
        sys.exit(1)
    elif args.get('track_name'):
        discogs_results = d.by_track(track_name=args.get('track_name'), artist=args.get('artist_name'))
        if len(discogs_results) == 0:
            print('Not found on discogs')
            sys.exit(0)
        if len(discogs_results) == 1:
            choice = 0
        else:
            print('[#] Artist - Album - Track -- Duration')
            for idx, entry in enumerate(discogs_results):
                print('[%d] %s' % (idx, entry))
            print('------------')
            choice = None
            while choice is None or choice < 0 or choice >= len(discogs_results):
                choice = input('Enter which track to download [between %d and %d]: ' % (0, len(discogs_results) - 1))
                choice = parse_int(choice)
        yt_dl_queue.append(discogs_results[choice])
    elif args.get('album_name'):
        discogs_masters = d.by_album(album_name=args.get('album_name'), artist=args.get('artist_name'))
        if len(discogs_masters) == 0:
            print('Not found on discogs')
            sys.exit(0)
        if len(discogs_masters) == 1:
            choice = 0
        else:
            print('[#] Artist - Album')
            for idx, master in enumerate(discogs_masters):
                artists = ', '.join(map(attrgetter('name'), master.main_release.artists))
                print('[%d] %s - %s' % (idx, artists, master.title))
            print('------------')
            choice = None
            while choice is None or choice < 0 or choice >= len(discogs_masters):
                choice = input('Enter which album/EP/etc. to download [between %d and %d]: ' % (0, len(discogs_masters) - 1))
                choice = parse_int(choice)
        yt_dl_queue.extend(entries_from_master(discogs_masters[choice]))
    else:
        print('You must search by one of either --track-name or --album-name')
        sys.exit(1)

    # Download queue from YouTube
    # TODO delete temp video file in case of exception
    for idx, discogs_entry in enumerate(yt_dl_queue):
        artists_str_truncated = ', '.join(discogs_entry.get_artists()[:3])
        if args['verbose']:
            print('\n\n-----\nSearching for %s - %s on YouTube (%d/%d)…' % (artists_str_truncated, discogs_entry.track.title, idx+1, len(yt_dl_queue)))
        yt_results = YouTubeSearch(artist=artists_str_truncated,
                                      song_title=discogs_entry.track.title)
        if len(yt_results.results) == 0:
            print('Not found on YouTube')
            sys.exit(0)
        prediction = yt_results.most_likely_result(ground_truth_duration=parse_string_duration(discogs_entry.track.duration))
        if args['verbose']:
            print('-----\nDownloading %s - %s from YouTube (watch?v=%s) (%d/%d)…' % (artists_str_truncated, discogs_entry.track.title, prediction.token, idx+1, len(yt_dl_queue)))
        filename = prediction.dl(output_directory=args['output_directory'], quiet=not args['verbose'])
        # Add ID3 tags
        if args['verbose']:
            print('-----\nAdding ID3 tags to %s - %s (%d/%d)…' % (artists_str_truncated, discogs_entry.track.title, idx+1, len(yt_dl_queue)))
        discogs_entry.to_id3_tags(filename)
        if args['verbose']:
            print('-----\nDone with %s - %s (%d/%d). Saved at %s' % (artists_str_truncated, discogs_entry.track.title, idx+1, len(yt_dl_queue), filename))
