from pathlib import Path


def path_reprocess(path):
    if type(path) == str:
        return Path(path)
    elif type(path) == Path:
        return path
    else:
        raise ValueError("Cannot handle the provided path.")
