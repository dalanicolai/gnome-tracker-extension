!!! IMPORTANT !!! For full functionality permissions must be changed on two files AFTER EVERY UPGRADE (unfortunately) Quick instructions below.

# Tracker/docfetcher deep file search
Ulauncher extension for deep search filesystem via the gnome tracker index. This extension additionally offers two easy customizable widgets using bash or python3 rexpectively for ulaction and appchooser.py

## Requirements (optional)

yad  
python3  
python gtk+ library (fedora -> python3-gobject, ubuntu -> python3-gi)

## Description

This extension provides filesystem deep search functionality via gnome tracker or docfetcher (respective keywords: gt and df) and near instant full system file search via the locate command (keyword: lc + 2x g for grep). Additionally it has an option to deep search files using the tracker search command which returns text snippets (keyword: ts). The output can be opened with your prefered application.

## Installation

Add the plugin via the extension menu in the ulauncher settings using the URL: https://github.com/dalanicolai/gnome-tracker-extension  

#### !!! THE FOLOWING ACTION MUST BE REPEATED AFTER EVERY UPDATE (UNFORTUNATELY) !!!
Subsequently navigate to the ~/.cache/ulauncher_cache/extensions/com.github.dalanicolai.gnome-tracker-extension directory and change permission to executable for the two files:

ulaction  
appchooser.py

(Right click the files in the file browser and check 'allow executing file as program' under properties -> permissions. Or issue "sudo chmod u+x filename" in the terminal)

### Choose action with yad dialog

If yad (available via the system repositories for most linux distributions) is not installed the extension will open the file in the application set as default in the system (using xdg-open).
If yad is installed, the extension will open a yad dialog offering different actions.

#### Open with dialog

The yad dialog offers an option to open a GTK+ 3 open with dialog. The script launching this dialog is written in python3 and uses the python3 gtk library.

### Contact

If you have any requests or comments relating to this extension than email me on dalanicolai@gmail.com
