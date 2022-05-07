"""
tulpar_cli/utils.py
Ian Kollipara
2022.04.05

Utility Definitions
"""

# Imports
from os.path import exists
from jinja2 import Environment, PackageLoader, select_autoescape
from rich.console import Console
from typer import Exit

template_env = Environment(
    loader=PackageLoader("tulpar_cli"),
    autoescape=select_autoescape(["py", "toml", "html"]),
)

def touch(filename: str, console: Console) -> None:
    """Create an empty file with the given filename.

    Given a filename, check if it exists or not. If it does
    then raise an exit command. Else create the empty file
    with that name.
    """

    if exists(filename):
        console.print("[bold red]file already exists")
        raise Exit(1)

    with open(filename, "w+", encoding="utf-8") as new_file:
        pass


def touch_and_render(filename: str, template_name: str, **template_args) -> None:
    """Create and write the templated file to the given filename.

    Given a valid template name and template args, write the newly rendered
    template to the given filename, if the file doesn't already exist.
    """

    new_file_data = template_env.get_template(template_name).render(template_args)

    with open(filename, "w", encoding="utf-8") as new_file:
        new_file.write(new_file_data)
