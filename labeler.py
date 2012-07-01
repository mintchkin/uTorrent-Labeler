import utorrentctl
import os.path
import argparse
from config import *


utorrent_connection = utorrentctl.uTorrentConnection(webui_config['host'], webui_config['login'], webui_config['password'])
utorrent = utorrentctl.uTorrent(utorrent_connection)


def set_label(hsh, label):
    utorrent.torrent_set_props([{hsh: {'label': label}}])


def label_from_tracker(hsh):
    trackers = utorrent.torrent_info(hsh)[hsh].trackers
    label = ['Other']

    for tracker in trackers:
        for announce in tracker_labels.keys():
            if announce in tracker:
                label = tracker_labels[announce]

    return label


def label_from_type(hsh):
    files = utorrent.file_list(hsh)[hsh]
    label = ['Other']

    for f in files:
        ext = os.path.splitext(f.name)[1]
        if ext in filetypes:
            label = filetypes[ext]

    return label


def smart_label(hsh):
    label = label_from_tracker(hsh)
    if label == ['Other']:
        label = label_from_type(hsh)
    return label


def smarter_label(hsh):
    tracker_labels_list = label_from_tracker(hsh)
    type_labels_list = label_from_type(hsh)

    if tracker_labels_list == ['Other']:
        return [type_labels_list[0]]
    elif type_labels_list == ['Other']:
        return [tracker_labels_list[0]]
    else:
        for tracker_label in tracker_labels_list:
            for type_label in type_labels_list:
                if type_label == tracker_label:
                    return [type_label]

    return ['No Label']


def label_all(method):
    for hsh in utorrent.torrent_list().keys():
        set_label(hsh, method(hsh)[0])


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Automatically label torrents.")
    parser.add_argument("hash", default="", nargs='?', help="Hash value of torrent to be labelled.")
    parser.add_argument("-a", "--all", action="store_true", help="Label all torrents using default smart_label.")
    parser.add_argument("-m", "--method", choices=['label_from_tracker', 'label_from_type', 'smart_label', 'smarter_label'], default='smarter_label', help="Method used for labeling.")
    parser.add_argument("-s", "--status", default="", help="Status of the torrent (to be passed by uTorrent); will only run if status is 'Downloading'.")

    args = parser.parse_args()
    print(args)

    methods = {'label_from_tracker': label_from_tracker,
               'label_from_type': label_from_type,
               'smart_label': smart_label,
               'smarter_label': smarter_label}

    if (args.hash or args.status) and args.all:
        print("Too many arguments.")
        exit(1)
    elif args.all:
        label_all(methods[args.method])
        exit(0)
    elif args.status and args.status != 'Downloading':
        print("Status is not Downloading")
        exit(1)
    elif args.hash:
        set_label(args.hash, method[args.method](args.hash))
        exit(0)
    else:
        parser.print_help()
