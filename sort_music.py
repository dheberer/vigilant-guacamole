#!/usr/bin/env python3

import sys
import os

import music_utils

print("Music Sort......")
file_lists = []
if len(sys.argv) != 4:
    print("creates a file structure that most music players want from ID3 tags")
    print("usage: sort_music.py [list | move] [artist | album] dir")
    exit()

action = sys.argv[1]
target = sys.argv[2]
target_dir = sys.argv[3]
if action not in ['list', 'move'] or target not in ['artist', 'album']:
    print("Invalid action or target, nothing done.")
    exit()

if action == 'list':
    things = []
    if target == 'artist':
        music_utils.set_empty_album_artists(target_dir)
        things = music_utils.get_album_artists(target_dir)
    if target == 'album':
        things = music_utils.get_albums(target_dir)
    for thing in things:
        print(thing)
