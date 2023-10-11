#! /usr/bin/env python3
'''
Manage save files from MemCardPro
'''
from datetime import datetime
from json import load as jload
from os import mkdir
from pathlib import Path
from re import sub
from shutil import copytree
from sys import argv
from urllib.request import urlopen
VERSION = '1.0.0'

# serial-to-title JSON URLs
JSON_URLS = {
    'PSX': 'https://github.com/niemasd/PSX-PS2-Save-Tools/raw/main/data/PSX.json',
    'PS2': 'https://github.com/niemasd/PSX-PS2-Save-Tools/raw/main/data/PS2.json',
    '???': 'https://github.com/niemasd/PSX-PS2-Save-Tools/raw/main/data/missing.json',
}

# folders to ignore
IGNORE = {'__MACOSX'}

# get current time as a string YYYY-MM-DD_HH-MM-SS
def get_time():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# convert a string to a safe folder name (replace unsafe symbols with '_')
def safe_name(s):
    return sub(r"[/\\?%*:|\"<>\x7F\x00-\x1F]", '_', s.strip())

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
    print("Welcome to the MemCard PRO Renamer v%s" % VERSION)
    try:
        # check user args
        if len(argv) == 1:
            argv.append(input("Drag folder here and hit ENTER: "))
        if len(argv) != 2:
            print("%s <folder>" % argv[0]); exit(1)
        orig_path = Path(argv[1].strip()).expanduser().absolute()
        if not orig_path.is_dir():
            raise ValueError("Folder not found: %s" % orig_path)

        # load JSONs
        print("Loading mapping of serial numbers to titles...")
        TITLE = load_jsons(JSON_URLS)

        # find game folders via DFS
        print("Scanning for game folders in: %s" % orig_path)
        game_folders = set(); to_explore = [orig_path]
        while len(to_explore) != 0:
            curr_path = to_explore.pop()
            if curr_path.is_dir() and curr_path.name not in IGNORE:
                to_explore += curr_path.glob('*')
            elif curr_path.is_file() and curr_path.name.lower().endswith('.mcd'):
                game_folders.add(curr_path.parent)
        print("Found %d game folder(s)" % len(game_folders))

        # rename game folders
        out_folder = 'renamed_%s' % get_time(); out_path = orig_path.parent.joinpath(out_folder)
        if out_path.is_dir() or out_path.is_file():
            raise ValueError("Output path exists: %s" % out_path)
        try:
            out_path.mkdir()
        except:
            out_path = Path.home().joinpath('Deskatop').joinpath(out_folder); out_path.mkdir()
        print("Copying renamed folders to: %s" % out_path)
        serial_not_found = list()
        for curr_path in game_folders:
            folder = curr_path.name.strip()
            if ' - ' in folder: # folder with title, so rename to MemCard PRO format
                memcard_folder = '-'.join(list(curr_path.glob('*.mcd'))[0].name.split('-')[:-1])
                copytree(curr_path, out_path.joinpath(safe_name(memcard_folder)))
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
                    copytree(curr_path, out_path.joinpath(safe_name('%s - %s' % (folder, curr_title))))

        # report any that failed to copy
        if len(serial_not_found) != 0:
            print("\nThe following serial numbers were not found in the database and were skipped:\n\n%s" % '\n'.join(serial_not_found))
            print("\nConsider submitting them to https://psxdatacenter.com")
    except Exception as e:
        print(str(e))
    input("\nPress ENTER to exit")
