#!/usr/bin/env python3
import os
from mutagen.easyid3 import EasyID3

def files_in_dir(path: str):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def _get_unique_tags(path: str, tag: str):
  files = files_in_dir(path)
  tags = set()

  for f in files:
    if not f.endswith('.mp3'):
      info = EasyID3(f)
      data = info[tag]
      if data == '' or data is None:
        data = 'Unknown'
      tags.add(data)
  return list(tags)

def get_album_artists(path: str):
  return _get_unique_tags(path, 'albumartist')

def get_albums(path: str):
  return _get_unique_tags(path, 'album')

def create_dirs(path: str, dirs):
  pass

def simple_deduplicate(path: str):
  duplicates = []
  files = files_in_dir(path)
  dup_ending = ' (1).mp3'
  for f in files:
    if f.endswith(dup_ending):
      og = f.replace(dup_ending, '.mp3')
      if og in files:
        duplicates.append(f)
      else:
        os.rename(os.path.join(path, f), os.path.join(path, og))
        print('Renamed ' + f)

  for f in duplicates:
    f = os.path.join(path, f)
    print('Removing ' + f)
    os.remove(f)

def create_artist_dirs(scan_path: str, dest_path) -> None:
  """
  This will look for all mp3 files in the scan_path recursively
  and build a list of unique names. Then it will write each of
  the found artists in the dest_path
  """

