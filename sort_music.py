#!/usr/bin/env python3

import sys
import os
from pathlib import Path
import music_utils

print("Music Sort......")
file_lists = []
if len(sys.argv) != 4:
    print("creates a file structure that most music players want from ID3 tags")
    print("usage: sort_music.py [list | move] [artist | album] dir")
    exit()

action = sys.argv[1]
kind = sys.argv[2]
source_dir = sys.argv[3]
destination_dir = os.path.join(source_dir, "sorted")
if action not in ['list', 'move'] or kind not in ['artist', 'album']:
    print("Invalid action or target, nothing done.")
    exit()

if action == 'list':
    things = []
    if kind == 'artist':
        music_utils.set_empty_album_artists(source_dir)
        things = music_utils.get_album_artists(source_dir)
    if kind == 'album':
        things = music_utils.get_albums(source_dir)
    for thing in things:
        print(thing)

if action == 'move':
    music_utils.set_empty_album_artists(source_dir)
    files = music_utils.files_in_dir(source_dir)
    for f in files:
        artist = music_utils.get_file_album_artist(f)
        album = music_utils.get_file_album_name(f)
        destiny = os.path.join(destination_dir, artist)
        if kind == 'album':
            destiny = os.path.join(destiny, album)
        Path(destiny).mkdir(parents=True, exist_ok=True)
        f_prime = os.path.join(destiny, os.path.basename(f))
        os.rename(src=f, dst=f_prime)
