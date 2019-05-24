# Tracker/docfetcher/locate deep file search
Ulauncher extension for deep search filesystem via the gnome tracker/docfetcher/locate index.

## Requirements

A running gnome-tracker daemon + tracker index (for gt and ts keywords)
A docfetcher daemon and index (for the df keyword)

A working daemon and index can be tested in the terminal using the 'tracker search' command (gt and ts) or with the docfetcher gui (df)  

## Description

This extension provides filesystem deep search functionality (i.e. full text search) via gnome tracker or docfetcher (respective keywords: gt and df) and near instant full system file search via the locate command (keyword: lc + 2x g for grep -i (see image)). Searching with gnome tracker by default searches on exact match, so optionally each pattern in the query can be appended with * as a wildcard (unfortunately I do not know how to use a wildcard in front of a SPARQL query). Additionally this extension has an option to deep search files using the tracker search command which returns text snippets (keyword: ts, also supports appending with * as wilcard). The output can be opened with your prefered application.

![screenshot from 2019-01-17 03-46-41](https://user-images.githubusercontent.com/18429791/51434764-aa3fdf80-1c68-11e9-89c7-6d147f514fd9.png)

## Usage

Type keyword followed by a search term. tracker (gt and ts) and docfetcher (df) by default search case-insensitive for matches with full words. However both allow to use wildcards (use symbol * ) at the and of a search term.

## Installation

Add the plugin via the extension menu in the ulauncher settings using the URL: https://github.com/dalanicolai/gnome-tracker-extension

## Short note on development

The py4j folder and the search.py file are part of docfetcher. They are required to use its search functionality from python. The appchooser.py is a small script that launches a gtk application chooser window. 

### Contact

If you have any requests or comments relating to this extension than email me on dalanicolai@gmail.com
