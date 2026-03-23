from pyprojroot import here
from pathlib import Path
from typing import Union, Callable, Iterable


def make_dir_function(
    dir_name: Union[str, Iterable[str]]
) -> Callable[..., Path]:
    """Generate a function that returns a path relative to the project root.

    Args:
        dir_name: Name of the subdirectory (or list of nested subdirectories)
            to append to the project root path.

    Returns:
        A function that accepts optional sub-path segments and returns
        the full Path relative to the project directory.
    """

    def dir_path(*args) -> Path:
        if isinstance(dir_name, str):
            return here().joinpath(dir_name, *args)
        else:
            return here().joinpath(*dir_name, *args)

    return dir_path


project_dir = make_dir_function("")

data_dir = make_dir_function("data")
data_raw_dir = make_dir_function(["data", "raw"])
data_processed_dir = make_dir_function(["data", "processed"])
data_interim_dir = make_dir_function(["data", "interim"])
data_external_dir = make_dir_function(["data", "external"])

models_dir = make_dir_function("models")
notebooks_dir = make_dir_function("notebooks")
references_dir = make_dir_function("references")

reports_dir = make_dir_function("reports")
reports_figures_dir = make_dir_function(["reports", "figures"])

config_dir = make_dir_function("config")