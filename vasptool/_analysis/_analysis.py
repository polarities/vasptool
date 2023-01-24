import fnmatch, os, difflib
from pathlib import Path
from vasprun import vasprun
import numpy as np
from numpy.lib import recfunctions as rfn
from tqdm import tqdm
from ..core._cfunc import path_reprocess
from ..handy_functions import get_files_from_path

def get_vasprunxml(path: str | Path):
    path = path_reprocess(path)
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, "vasprun.xml"):
            matches.append(os.path.join(root, filename))
    return matches

def pull_data_from_vasprunxml(working_path, folder_delimiter, folder_col_dtype, vasprun_attributes, vasprun_col_dtype):
    vrun = get_vasprunxml(working_path)
    master_list = list()
    dtype_obj = list()
    if len(vasprun_attributes) != len(vasprun_col_dtype):  # If size of dtype-like tuple is not matching with attribute.
        raise ValueError("Length of `vasprun_col_dtype` and `vasprun_attributes` are not matches each others.")

    for vrunpath in tqdm(vrun, total=len(vrun)):  # Loop over found vasprun.xml files.
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

def diff_pprint(differ_compared, reference:str, compared:str, localize=False):
    BLUE = '\033[94m'
    RED = '\033[31m'
    GREEN = '\033[92m'
    ENDC = '\033[0m'

    print(BLUE + 'Reference: ' + reference + ENDC)
    print(BLUE + ' Compared: ' + compared + ENDC)

    idx = 0
    for line in differ_compared:
        if line[0:2] == '  ':
            pass
        elif line[0:2] == '? ':
            if prev == 1:
                COL = RED
            elif prev == 2:
                COL = GREEN
            if localize:
                print("\t" + COL + line.strip() + ENDC)
            idx += 1
        elif line[0:2] == '- ':
            print("\t" +RED + line.strip() + ENDC)
            idx += 1
            prev = 1
        elif line[0:2] == '+ ':
            print("\t" +GREEN + line.strip() + ENDC)
            idx += 1
            prev = 2
    if idx == 0:
        print(RED + "  Reference and given documents are identical" + ENDC)
    del differ_compared

def filediff(path:str, fname:str, reference_indice=-1):
    differ = difflib.Differ()
    file_list = get_files_from_path(path=path, fname=fname)
    reference = file_list.pop(reference_indice)
    with open(reference) as ref:
        ref_lines = ref.readlines()
    for file in file_list:
        with open(file) as com:
            comp_lines = com.readlines()
        diff = differ.compare(
            a=ref_lines,
            b=comp_lines,
        )
        diff_pprint(diff, reference, file)