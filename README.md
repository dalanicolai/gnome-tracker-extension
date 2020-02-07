![Extension logo](images/detective_penguin.png) image source: www.wpclipart.com

# Tracker/recoll/docfetcher/locate/ deep file search + calibre database search
Ulauncher extension for deep searching the filesystem or the calibre database via the recoll / gnome tracker / docfetcher / locate index or calibre database file and handle the results in multiple ways (e.g. opening in default application).


#### If you like this extension then consider to star it on github so people can find it more easily (by sorting on github stars on the ulauncher extension page)  

## Requirements

A running gnome-tracker daemon + tracker index (for gt and ts keywords)
A recoll index and the recoll python api (for the rc keyword)
A docfetcher daemon and index (for the df keyword)

A working daemon and index can be tested respectively in the terminal using the `tracker search` command (gt and ts), with the recoll gui (rc) or with the docfetcher gui (df)  

A calibre sqlite database file (for the cb keyword)


## Description

This extension provides filesystem deep search functionality (i.e. full text search) via gnome tracker, recoll or docfetcher (respective keywords: gt, rc and df) and near instant full system file search via the locate command (keyword: lc + 2x g for grep -i (see image)). Additionally it provides functionality to search books in the calibre database. Searching with gnome tracker by default searches on exact match, so optionally each pattern in the query can be appended with * as a wildcard (unfortunately I do not know how to use a wildcard in front of a SPARQL query). Additionally this extension has an option to deep search files using the tracker search command which returns text snippets (keyword: ts, also supports appending with * as wilcard). The output can be opened with your prefered application.

![screenshot from 2019-01-17 03-46-41](https://user-images.githubusercontent.com/18429791/51434764-aa3fdf80-1c68-11e9-89c7-6d147f514fd9.png)


## Usage

### Tracker/recoll/docfetcher and locate keywords

Type keyword followed by a search term. Tracker (default: gt and ts), recoll (default: rc) and docfetcher (default: df) by default search case-insensitive for matches with full words. However all these keywords allow to use wildcards (use symbol * ) at the and of a search term. As the tracker and recoll searches can return many results these searches can be narrowed down by an single grep using g followed by the keyword (see image) where the grep works only on the filename field. The locate keyword can be extended twice with a grep using g keyword (see image). 

#### Use wildcards by default

The extension has a setting option to use wildcards by default (there is no extended grep functionality for the tracker keyword here). 

#### Documentation recoll query syntax

The rc keyword supports the very powerful recoll query syntax as documented [here](https://www.lesbonscomptes.com/recoll/usermanual/webhelp/docs/RCL.SEARCH.LANG.html)

### Calibre keyword

The calibre keyword (default: cb) searches in the title and author_sort (**can be different from te author field,** see book's metadata) fields and can handle two query patterns separated by a space (e.g. "cb hello dan") where the search is case insensitive and includes wildcards before and after the patterns.


## Installation

Add the plugin via the extension menu in the ulauncher settings using the URL: https://github.com/dalanicolai/gnome-tracker-extension


## Short note on development

* The py4j folder and the search.py file are part of docfetcher. They are required to use its search functionality from python. If a user wishes that the docfetcher keywords also gets a grep extension functionality (like the tracker, recoll and locate keywords), then someone who knows python can either implement this functionality easily himself or another user can simply open an issue on github or send me a request by mail (see below). 

* The appchooser.py is a small script that launches a gtk application chooser window. 

* This extension might be useful to use as a template for other seach extensions. Also, if you know some python, its (search) behavior can be easily adapted to you own preferences by adapting the code in main.py.

### Contact

To report any bugs or if you have any requests or comments relating to this extension send an e-mail to dalanicolai@gmail.com, or just open an issue here on github.
