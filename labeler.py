import utorrentctl
import os.path
import argparse
from config import *


utorrent_connection = utorrentctl.uTorrentConnection(webui_config['host'], webui_config['login'], webui_config['password'])
utorrent = utorrentctl.uTorrent(utorrent_connection)


def set_label(hsh, label):
    utorrent.torrent_set_props([{hsh: {'label': label}}])


def label_from_tracker(hsh):
    """Returns a list of labels based on the torrent trackers
    and 'trackers' data in config.py, else returns default_label"""
    torrent_trackers = utorrent.torrent_info(hsh)[hsh].trackers
    label = []

    for torrent_tracker in torrent_trackers:
        for tracker_name in trackers.keys():
            if tracker_name in torrent_tracker and trackers[tracker_name] not in label:
                label += trackers[tracker_name]

    if len(label) == 0:
        label = default_label

    return label


def label_from_type(hsh):
    """Returns a list of labels based on the extensions of
    files in torrent and 'filetypes' data in config.py, else
    returns default_label"""
    files = utorrent.file_list(hsh)[hsh]
    label = []

    for f in files:
        ext = os.path.splitext(f.name)[1].lower()
        if ext in filetypes:
            for item in filetypes[ext]:
                if item not in label:
                    label += filetypes[ext]

    if len(label) == 0:
        label = default_label

    return label


def safe_label(hsh):
    """Uses label_from_type and label_from_tracker to only return
    a label if it is certain, else returns default_label"""
    type_labels = label_from_type(hsh)
    tracker_labels = label_from_tracker(hsh)

    if len(tracker_labels) == 1 and tracker_labels != default_label:
        return tracker_labels
    elif len(type_labels) == 1 and type_labels != default_label:
        return type_labels
    else:
        return default_label


def smart_label(hsh):
    """A smart label that uses label_from_type and label_from_tracker
    to make a "best guess" whenever possible, else returns default_label"""
    label = label_from_tracker(hsh)
    if label == default_label:
        label = label_from_type(hsh)
    return label


def smarter_label(hsh):
    """Returns a more accurate "best guess" in slightly more possible cases than
    smart_label. Probably should always be used over smart_label"""
    type_labels = label_from_type(hsh)
    tracker_labels = label_from_tracker(hsh)
    label = []

    if type_labels == default_label:
        label = tracker_labels
    elif tracker_labels == default_label:
        label = type_labels
    else:
        for tracker_label in tracker_labels:
            for type_label in type_labels:
                if type_label == tracker_label:
                    label.append(type_label)

        if len(label) == 0:
            label = default_label

    return label


def label_all(method):
    for hsh in utorrent.torrent_list().keys():
        set_label(hsh, method(hsh)[0])


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Automatically label torrents.")
    parser.add_argument("hash", default="", nargs='?', help="Hash value of torrent to be labelled.")
    parser.add_argument("-a", "--all", action="store_true", help="Label all torrents using default smart_label.")
    parser.add_argument("-m", "--method", choices=['label_from_tracker', 'label_from_type', 'safe_label', 'smart_label', 'smarter_label'], default='safe_label', help="Method used for labeling.")
    parser.add_argument("-s", "--status", default="", help="Status of the torrent (to be passed by uTorrent); will only run if status is 'Downloading'.")

    args = parser.parse_args()
    print(args)

    methods = {'label_from_tracker': label_from_tracker,
               'label_from_type': label_from_type,
               'safe_label': safe_label,
               'smart_label': smart_label,
               'smarter_label': smarter_label}

    if (args.hash or args.status) and args.all:
        print("ERROR: Too many arguments.")
        exit(1)
    elif args.all:
        label_all(methods[args.method])
        exit(0)
    elif args.status and args.status != 'Downloading':
        print("ERROR: Status is not Downloading")
        exit(1)
    elif args.hash:
        set_label(args.hash, methods[args.method](args.hash)[0])
        exit(0)
    else:
        parser.print_help()
