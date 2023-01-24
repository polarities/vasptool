import fnmatch
import os
import shutil
from pathlib import Path
from vasprun import vasprun
import numpy as np
from numpy.lib import recfunctions as rfn
from tqdm import tqdm

def path_reprocess(path):
    if type(path) == str:
        return Path(path)
    elif type(path) == Path:
        return path
    else:
        raise ValueError("Cannot handle the provided path.")


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


def pull_data_from_vasprunxml(working_path, folder_delimiter, folder_col_dtype, vasprun_attributes, vasprun_col_dtype):
    vrun = get_vasprunxml(working_path)
    master_list = list()
    dtype_obj = list()
    if len(vasprun_attributes) != len(vasprun_col_dtype):  # If size of dtype-like tuple is not matching with attribute.
        raise ValueError("Length of `vasprun_col_dtype` and `vasprun_attributes` are not matches each others.")

    for vrunpath in tqdm(vrun):  # Loop over found vasprun.xml files.
        temporary_list = list()
        # Check folder name format is matching with the given dtype-like tuple.
        if len(folder_values := vrunpath.split('/')[-2].split(sep=folder_delimiter)) == len(folder_col_dtype):
            # If different, raises error.
            if len(folder_values) != len(folder_col_dtype):
                raise ValueError("Length of `folder_col_dtype` is not matches with the number of array parsed from "
                                 "folder name.")
            fvalue = list()
            try:  # When error
                for idx, folder_dtype in enumerate(folder_col_dtype):  # Convert to the specified type.
                    fvalue += [folder_dtype[1](folder_values[idx]), ]
            except KeyError:
                fvalue = None
            temporary_list += fvalue

        vddd = vasprun(vrunpath).values  # vasprun.xml file content in dictionary
        for idx, attribute in enumerate(vasprun_attributes):  # recursive query based on the key path.
            keys = attribute.split('/')
            for key in keys:
                vddd = vddd[key]
            queried_value = vddd
            temporary_list += [vasprun_col_dtype[idx][1](queried_value), ]  # Convert to the desired type.
        master_list.append(temporary_list)
    dtype_obj += folder_col_dtype  # Construct dtype.
    dtype_obj += vasprun_col_dtype  # Construct dtype.
    return rfn.unstructured_to_structured(np.array(master_list), dtype=np.dtype(dtype_obj))  # Returns structured array.
