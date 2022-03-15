#!/usr/bin/env python3
import os

def files_in_dir(path: str):
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def get_artists(path: str):
  return []

def get_albums(path: str):
  return []

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


