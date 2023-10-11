#! /usr/bin/env python3
'''
Manage save files from MemCardPro
'''
from datetime import datetime
from glob import glob
from json import load as jload
from os import mkdir
from os.path import basename, dirname, isdir, isfile, join
from shutil import copytree
from sys import argv
from urllib.request import urlopen

# serial-to-title JSON URLs
JSON_URLS = {
    'PSX': 'https://github.com/niemasd/PSX-PS2-Save-Tools/raw/main/data/PSX.json',
    'PS2': 'https://github.com/niemasd/PSX-PS2-Save-Tools/raw/main/data/PS2.json',
}

# folders to ignore
IGNORE = {'__MACOSX'}

# get current time as a string YYYY-MM-DD_HH-MM-SS
def get_time():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

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

# main program
if __name__ == "__main__":
    # check user args
    if len(argv) == 1:
        argv.append(input("Drag folder here and hit ENTER: "))
    if len(argv) != 2:
        print("%s <folder>" % argv[0]); exit(1)
    argv[1] = argv[1].rstrip('/').rstrip('\\')
    if not isdir(argv[1]):
        raise ValueError("Folder not found: %s" % argv[1])

    # load JSONs
    print("Loading mapping of serial numbers to titles...")
    TITLE = load_jsons(JSON_URLS)

    # find game folders via DFS
    print("Scanning for game folders in: %s" % argv[1])
    game_folders = set(); to_explore = [argv[1]]
    while len(to_explore) != 0:
        curr_path = to_explore.pop()
        if isdir(curr_path) and curr_path not in IGNORE:
            to_explore += list(glob(join(curr_path, '*')))
        elif isfile(curr_path) and curr_path.lower().endswith('.mcd'):
            game_folders.add(dirname(curr_path))
    print("Found %d game folder(s)" % len(game_folders))

    # rename game folders
    out_path = join(argv[1], '..', 'renamed_%s' % get_time())
    if isfile(out_path) or isdir(out_path):
        raise ValueError("Output path exists: %s" % out_path)
    mkdir(out_path); serial_not_found = list()
    for curr_path in game_folders:
        folder = basename(curr_path).strip()
        if ' - ' in folder: # folder with title, so rename to MemCard PRO format
            memcard_folder = '-'.join(basename(list(glob(join(curr_path, '*.mcd')))[0]).split('-')[:-1])
            copytree(curr_path, join(out_path, memcard_folder))
        else:               # folder without title, so rename to human-readable
            folder_upper = folder.upper(); curr_title = None
            if folder_upper in TITLE:
                curr_title = TITLE[folder_upper]
            else: # brute force search
                for serial, title in TITLE.items():
                    if serial.upper() in folder_upper:
                        curr_title = title; break
            if curr_title is None:
                serial_not_found.append(folder_upper)
            else:
                copytree(curr_path, join(out_path, '%s - %s' % (folder, curr_title)))

    # report any that failed to copy
    if len(serial_not_found) != 0:
        print("\nThe following serial numbers were not found in the database and were skipped:\n\n%s" % '\n'.join(serial_not_found))
        print("\nConsider submitting them to https://psxdatacenter.com")
        input("\nPress ENTER to exit")
