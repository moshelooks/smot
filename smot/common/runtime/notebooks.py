import os

from smot.common import str_fns
from smot.common.runtime import build_paths, reflection


def notebook_path() -> str:
    return os.path.realpath("__file__")


def notebook_dir() -> str:
    return os.path.dirname(notebook_path())


def notebook_relative_dir() -> str:
    return str_fns.removeprefix(
        notebook_dir(),
        reflection.repository_source_root() + "/",
    )


def output_path(name: str) -> str:
    d = os.path.join(
        build_paths.build_root(),
        notebook_relative_dir(),
    )
    os.makedirs(d, exist_ok=True)
    return os.path.join(
        d,
        name,
    )
