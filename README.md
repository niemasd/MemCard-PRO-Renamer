[**`memcard_pro_renamer.py`**](memcard_pro_renamer.py) is a cross-platform pure-Python script for renaming MemCard PRO save folders. Just do the following:

1. Download the [`memcard_pro_renamer.py`](memcard_pro_renamer.py) script to your computer
2. Run the script (e.g. double-click)
3. Drag-and-drop the folder that contains all of your game save folders (or manually type it if drag-and-drop doesn't work on your machine)
4. Hit `ENTER`, and the tool will create a renamed copy of each of your game save folders (to avoid accidentally overwriting and breaking something)

It'll load the latest [PSX](data/PSX.json) and [PS2](data/PS2.json) serial number to title mappings (obtained from [The Playstation Datacenter](https://psxdatacenter.com/)), and it'll automatically rename your game folders.

* If your game save folders are in the original `SXXX-XXXXX` serial number format, it'll rename them to `SXXX-XXXXX - GAME TITLE`
* If your game save folders are already in the renamed `SXXX-XXXXX - GAME TITLE` format, it'll rename them back to the `SXXX-XXXXX` serial number format

You'll need [Python](https://www.python.org/) installed on your machine to run this script, and it should work on any operating system out-of-the-box.
