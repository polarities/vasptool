import fnmatch
import os
import shutil
from pathlib import Path
from vasprun import vasprun
import numpy as np
from numpy.lib import recfunctions as rfn


def path_reprocess(path):
    if type(path) == str:
        return Path(path)
    elif type(path) == Path:
        return path
    else:
        raise ValueError("Cannot handle the provided path.")

def get_vasprunxml(path):
    path = path_reprocess(path)
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, "vasprun.xml"):
            matches.append(os.path.join(root, filename))
    return matches

def get_files_from_path(path, fname):
    path = path_reprocess(path)
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, fname):
            matches.append(os.path.join(root, filename))
    return matches

def mkdir_if_not_exist(path, clean_content=False):
    path = path_reprocess(path)
    if os.path.exists(path):
        if clean_content == True:
            shutil.rmtree(path)
    else:
        os.mkdir(path)


def pull_data_from_vasprunxml(working_path, folder_delimiter, folder_col_dtype, vasprun_attributes, vasprun_col_dtype):
    vrun = get_vasprunxml(working_path)
    master_list = list()
    dtype_obj = list()
    for vrunpath in vrun:
        temporary_list = list()
        if len(folder_values:=vrunpath.split('/')[-2].split(sep=folder_delimiter)) == len(folder_col_dtype):
            fvalue = list()
            for idx, folder_dtype in enumerate(folder_col_dtype):
                fvalue += [folder_dtype[1](folder_values[idx]), ]
            temporary_list += fvalue

        vddd = vasprun(vrunpath).values
        for idx, attribute in enumerate(vasprun_attributes):
            keys = attribute.split('/')
            for key in keys:
                vddd = vddd[key]
            queried_value = vddd
            temporary_list += [vasprun_col_dtype[idx][1](queried_value), ]
        master_list.append(temporary_list)
    dtype_obj += folder_col_dtype
    dtype_obj += vasprun_col_dtype

    return rfn.unstructured_to_structured(np.array(master_list), dtype=np.dtype(dtype_obj))