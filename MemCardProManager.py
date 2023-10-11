#! /usr/bin/env python3
'''
Manage save files from MemCardPro
'''
from glob import glob
from json import load as jload
from os import getcwd, name as os_name, system
from os.path import abspath, expanduser, isdir, isfile
from urllib.request import urlopen

# serial-to-title JSON URLs
JSON_URLS = {
    'PSX': 'https://github.com/niemasd/PSX-PS2-Save-Tools/raw/main/data/PSX.json',
    'PS2': 'https://github.com/niemasd/PSX-PS2-Save-Tools/raw/main/data/PS2.json',
}

# load serial-to-title mapping
def load_jsons(json_urls):
    out = dict()
    for url in json_urls.values():
        try:
            curr = jload(urlopen(url))
        except:
            raise RuntimeError("Failed to load: %s" % url)
        for k,v in curr.items():
            out[k.strip().upper()] = v.strip().upper()
    return out

# clear terminal screen
def clear_screen():
    system('cls' if os_name == 'nt' else 'clear')

# select path
def select_path(curr_path):
    clear_screen()
    print("CURRENT PATH: %s\n" % curr_path)
    dirs = list(); files = list()
    for fn in glob('%s/*' % curr_path):
        if isdir(fn):
            dirs.append(fn)
        elif isfile(fn) and fn.lower().endswith('.mcd'):
            files.append(fn)
    children = sorted(dirs, key=lambda x: x.lower()) + sorted(files, key=lambda x: x.lower())
    for i, fn in enumerate(children):
        tmp = fn.split('/')[-1]
        if isdir(fn):
            tmp += '/'
        print("(%d) %s" % (i+1, tmp))
    print()
    while True:
        try:
            out = children[int(input("Select file/folder: "))-1]; break
        except:
            pass
    return out

# main program
if __name__ == "__main__":
    TITLE = load_jsons(JSON_URLS)
    start_path = abspath(expanduser(getcwd())).rstrip('/')
    curr_path = start_path
    print("SELECTED: %s" % select_path(curr_path))
