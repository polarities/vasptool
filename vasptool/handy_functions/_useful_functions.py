import fnmatch
import os
import shutil
from pathlib import Path
from ..core._cfunc import path_reprocess
import math
import numpy as np


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


def mkdir_if_not_exist(path: str | Path, clean_content: bool = False):
    path = path_reprocess(path)
    if os.path.exists(path):
        if clean_content == True:
            shutil.rmtree(path)
    else:
        os.mkdir(path)


def generate_divisors(n):
    large_divisors = []
    for i in range(1, int(math.sqrt(n) + 1)):
        if n % i == 0:
            yield i
            if i * i != n:
                large_divisors.append(n / i)
    for divisor in reversed(large_divisors):
        yield divisor


def node_cpu_npar(ncpu, core_per_node: int = 48):
    node = int(math.ceil(ncpu / core_per_node))
    cpu = int(ncpu / node)
    divisor = np.array(list(generate_divisors(ncpu)))
    distance = np.abs(divisor - math.sqrt(cpu))
    min_dist = divisor[np.where(distance == np.min(distance))]

    if ncpu != node * cpu:
        raise Exception("Automatic estimation failed.")

    return node, cpu, int(min_dist)
