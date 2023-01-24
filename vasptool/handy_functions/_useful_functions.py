import fnmatch
import os
import shutil
from pathlib import Path
from ..core._cfunc import path_reprocess


def get_vasprunxml(path: str | Path):
    path = path_reprocess(path)
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, "vasprun.xml"):
            matches.append(os.path.join(root, filename))
    return matches


def get_files_from_path(path: str | Path, fname: str):
    path = path_reprocess(path)
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, fname):
            matches.append(os.path.join(root, filename))
    return matches


def mkdir_if_not_exist(path: str | Path, clean_content:bool=False):
    path = path_reprocess(path)
    if os.path.exists(path):
        if clean_content == True:
            shutil.rmtree(path)
    else:
        os.mkdir(path)



