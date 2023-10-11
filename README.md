# MemCard PRO Renamer

[**`memcard_pro_renamer.py`**](https://github.com/niemasd/MemCard-PRO-Renamer/releases/latest/download/memcard_pro_renamer.py) is a cross-platform pure-Python script for renaming MemCard PRO save folders. Just do the following:

1. Download the [`memcard_pro_renamer.py`](https://github.com/niemasd/MemCard-PRO-Renamer/releases/latest/download/memcard_pro_renamer.py) script to your computer
2. Run the script (e.g. double-click)
3. Drag-and-drop the folder that contains all of your game save folders (or manually type it if drag-and-drop doesn't work on your machine)
4. Hit `ENTER`, and the tool will create a renamed copy of each of your game save folders (to avoid accidentally overwriting and breaking something)

It'll load the latest [PSX](data/PSX.json) and [PS2](data/PS2.json) serial number to title mappings (obtained from [The Playstation Datacenter](https://psxdatacenter.com/)), and it'll automatically rename your game folders.

* If your game save folders are in the original `SXXX-XXXXX` serial number format, it'll rename them to `SXXX-XXXXX - GAME TITLE` so you can back them up in a human-readable format
* If your game save folders are already in the renamed `SXXX-XXXXX - GAME TITLE` format, it'll rename them back to the `SXXX-XXXXX` serial number format so you can restore them back onto the MemCard PRO

You'll need Python installed on your machine to run this script, and it *should* hopefully work on any operating system out-of-the-box. If not, please feel free to create a [GitHub Issue](https://github.com/niemasd/MemCard-PRO-Renamer/issues) with info about your computer's operating system / environment, and I can try to help figure it out :-)

# OS-Specific Notes
## Windows
Instead of installing Python from [python.org](https://www.python.org), which doesn't seem to work with double-click out-of-the-box (it seems to just instantly close the command prompt that gets opened), try installing Python through the [Microsoft Store](https://apps.microsoft.com/detail/python-3-11/9NRWMJP3717K).
