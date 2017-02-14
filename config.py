#!/usr/bin/env python3

webui_config = {'host': 'localhost:YOUR_WEBUI_PORT',
                'login': 'YOUR_WEBUI_LOGIN',
                'password': 'YOUR_WEBUI_PASSWORD'}

# Holds the list of trackers and the label types associated with
# them. If possible, the list of possible labels for each tracker
# should be in decending order of likelyhood (for example, if most
# of the torrents you download from a given tracker are type X, with
# only a few being type Y, then your list should be [X, Y])
#
# Format: trackers = {'TRACKERNAME': ['LABEL1', 'LABEL2', ...], ...}
trackers = {'tehconnection': ['Movies', 'DVDRs'],
            'passthepopcorn': ['Movies', 'DVDRs'],
            'bitgamer': ['Games'],
            'what': ['Music', 'Applications'],
            'broadcasthe': ['TV Shows']}

# Holds the list of file extensions and the label types associated
# with them. See above about the order of the labels list.
#
# Format: filetypes = {'.EXTENSION': ['LABEL1', 'LABEL2', ...], ...}
filetypes = {'.mkv': ['Movies', 'TV Shows'],
             '.mp4': ['Movies', 'TV Shows'],
             '.avi': ['TV Shows', 'Movies'],
             '.m4v': ['TV Shows', 'Movies'],
             '.rar': ['Applications', 'Games'],
             '.exe': ['Applications', 'Games'],
             '.iso': ['DVDRs', 'Applications'],
             '.vob': ['DVDRs'],
             '.mp3': ['Music'],
             '.flac': ['Music']}

# Defines the default label that will be used if a match cannot be found.
default_label = ['Other']