# Tracker/recoll/docfetcher/locate/ deep file search + calibre database search
Ulauncher extension for deep search filesystem and calibre database via the gnome tracker / docfetcher / locate index and calibre database file, handle the results in multiple ways (e.g. opening in default application).

#### If you like this extension then consider to star it on github so people can find it more easily (by sorting on github stars on the ulauncher extension page)  

## Requirements

A running gnome-tracker daemon + tracker index (for gt and ts keywords)
A recoll index and the recoll python api (for the rc keyword)
A docfetcher daemon and index (for the df keyword)

A working daemon and index can be tested respectively in the terminal using the 'tracker search' command (gt and ts), with the recoll gui (rc) or with the docfetcher gui (df)  

A calibre sqlite database file (for the cb keyword)

## Description

This extension provides filesystem deep search functionality (i.e. full text search) via gnome tracker, recoll or docfetcher (respective keywords: gt, rc and df) and near instant full system file search via the locate command (keyword: lc + 2x g for grep -i (see image)). Additionally it provides functionality to search books in the calibre database. Searching with gnome tracker by default searches on exact match, so optionally each pattern in the query can be appended with * as a wildcard (unfortunately I do not know how to use a wildcard in front of a SPARQL query). Additionally this extension has an option to deep search files using the tracker search command which returns text snippets (keyword: ts, also supports appending with * as wilcard). The output can be opened with your prefered application.

![screenshot from 2019-01-17 03-46-41](https://user-images.githubusercontent.com/18429791/51434764-aa3fdf80-1c68-11e9-89c7-6d147f514fd9.png)

## Usage

Type keyword followed by a search term. Tracker (default: gt and ts), recoll (default: rc) and docfetcher (default: df) by default search case-insensitive for matches with full words. However all allow to use wildcards (use symbol * ) at the and of a search term. The locate keyword can be extended twice with a grep using g keyword (see image). 

The calibre keyword (default: cb) searches in the title and author_sort (**can be different from te author field,** see book's metadata) fields and can handle two query patterns separated by a space (e.g. "cb hello dan") and the search is case insensitive and includes wildcards before and after the patterns.


## Installation

Add the plugin via the extension menu in the ulauncher settings using the URL: https://github.com/dalanicolai/gnome-tracker-extension

## Short note on development

The py4j folder and the search.py file are part of docfetcher. They are required to use its search functionality from python. The appchooser.py is a small script that launches a gtk application chooser window. 

This extension might be useful to use as a template for other seach extensions. Also, if you know some python, its (search) behavior can be easily adapted to you own preferences by adapting the code in main.py.

### Contact

If you have any requests or comments relating to this extension than email me on dalanicolai@gmail.com
