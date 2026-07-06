"""Load/dump json, yaml and pickle files from the local (hard disk) backend."""

import json
import pickle
from pathlib import Path
from typing import Any

import yaml

try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader  # type: ignore

FILE_FORMAT_TO_MODE = {
    "json": "text",
    "yaml": "text",
    "yml": "text",
    "pickle": "binary",
    "pkl": "binary",
}


def infer_file_format(file: str | Path, file_format: str | None) -> str:
    if file_format is None:
        file_format = str(file).split(".")[-1]
    if file_format not in FILE_FORMAT_TO_MODE:
        raise TypeError(f"Unsupported format: {file_format}")
    return file_format


def load(file: str | Path, file_format: str | None = None, **kwargs) -> Any:
    """Load data from a json/yaml/pickle file on the local filesystem.

    Args:
        file (str or :obj:`Path`): Path of the file to load.
        file_format (str, optional): If not specified, the file format will
            be inferred from the file extension. Currently supported formats
            include "json", "yaml"/"yml" and "pickle"/"pkl".

    Returns:
        Any: The content loaded from the file.
    """
    file_format = infer_file_format(file, file_format)
    mode = "rb" if FILE_FORMAT_TO_MODE[file_format] == "binary" else "r"

    with open(file, mode) as f:
        if file_format == "json":
            return json.load(f, **kwargs)
        if file_format in ("yaml", "yml"):
            kwargs.setdefault("Loader", Loader)
            return yaml.load(f, **kwargs)
        return pickle.load(f, **kwargs)


def dump(
    obj: Any,
    file: str | Path | None = None,
    file_format: str | None = None,
    **kwargs,
) -> str | bytes | None:
    """Dump data as a json/yaml/pickle string or to a file on disk.

    Args:
        obj (Any): The python object to be dumped.
        file (str or :obj:`Path`, optional): If not specified, the object is
            dumped to a string/bytes and returned, otherwise written to the
            given path.
        file_format (str, optional): Same as :func:`load`. Required when
            ``file`` is not given, otherwise inferred from its extension.

    Returns:
        The dumped string/bytes when ``file`` is not given, ``None``
        otherwise.
    """
    if file_format is None:
        if file is not None:
            file_format = str(file).split(".")[-1]
        else:
            raise ValueError("file_format must be specified since file is None")
    if file_format not in FILE_FORMAT_TO_MODE:
        raise TypeError(f"Unsupported format: {file_format}")

    if file_format == "json":
        if file is None:
            return json.dumps(obj, **kwargs)
        with open(file, "w") as f:
            json.dump(obj, f, **kwargs)
            return None

    if file_format in ("yaml", "yml"):
        kwargs.setdefault("Dumper", Dumper)
        if file is None:
            return yaml.dump(obj, **kwargs)
        with open(file, "w") as f:
            yaml.dump(obj, f, **kwargs)
            return None

    kwargs.setdefault("protocol", 2)
    if file is None:
        return pickle.dumps(obj, **kwargs)
    with open(file, "wb") as f:
        pickle.dump(obj, f, **kwargs)
        return None
