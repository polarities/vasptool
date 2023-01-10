import fnmatch
import os

def get_vasprunxml(path):
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, "vasprun.xml"):
            matches.append(os.path.join(root, filename))
    return matches

def get_files_from_path(path, fname):
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, fname):
            matches.append(os.path.join(root, filename))
    return matches
