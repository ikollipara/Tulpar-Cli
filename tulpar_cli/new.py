"""
tulpar_cli/new.py
Ian Kollipara
2022.04.05

New Command
"""

# Imports

from datetime import date
from os import chdir, mkdir
from os.path import exists
from functools import partial
import requests

from jinja2 import PackageLoader
from rich import get_console
from typer import Argument, Exit, Option

from .utils import template_env, touch as util_touch, touch_and_render as util_touch_and_render
from .app import tulpar

console = get_console()

touch = partial(util_touch, console=console)
touch_and_render = partial(util_touch_and_render, console=console)

@tulpar.command("new")
def new_project(
    project_name: str = Argument(..., help="Name of Tulpar project", metavar="NAME"),
    flat: bool = Option(False, "--flat", "-f", help="Initialize in current directory"),
    dry_run: bool = Option(
        False, "--dry-run", help="Show output, but don't create anything"
    ),
):
    """Create a new Tulpar Project

    Initialize a new Tulpar Project. Tulpar uses Poetry for handling dependencies, and will create a
    pyproject.toml file for your application. Tulpar has a set file structure:
    ```
    tests/
      | __init__.py
      | conftest.py
    <app>/
      | __init__.py
      | app.py
      | config.py
      assets/
      hooks/
      middleware/
      orm/
      pages/
      resources/
      services/
      templates/
    ```
    """

    app_dir_name = project_name.replace("-", "_")

    if not flat:
        if exists(project_name):
            console.print(f"[bold red]{project_name} directory already exists")
            raise Exit(1)

        mkdir(project_name)
        chdir(project_name)
    

    mkdir("tests")

    touch("tests/conftest.py")
    touch("tests/__init__.py")

    console.print("[bold blue]tests directory is initialized")

    mkdir(app_dir_name)
    chdir(app_dir_name)

    for dir in (
        "services",
        "pages",
        "resources",
        "orm",
        "middleware",
        "hooks",
        "templates",
        "assets"
    ):
        mkdir(dir)

    touch("__init__.py")
    # Default Args
    date_str = date.today().strftime("%Y.%m.%d")

    console.print(f"[bold green]{app_dir_name} directory has been initialized")


    touch_and_render("app.py", "app.py.jinja", date=date_str)
    console.print("[bold cyan]Creating app.py file")
    

    touch_and_render(
        "config.py",
        "config.py.jinja",
        date=date_str,
        app_name=" ".join(map(str.capitalize, project_name.split("-"))),
    )
    console.print("[bold cyan]Creating config.py file")


    touch_and_render(
        "../pyproject.toml", "pyproject.toml.jinja", app_name=project_name
    )
    console.print("[bold cyan]Creating pyproject.toml file")

    touch_and_render(
        "pages/index.py", "page.py.jinja", file_name="index", date=date_str
    )
    console.print("[bold cyan]Creating pages/index.py file")

    touch_and_render(
        "resources/hello.py",
        "resource.py.jinja",
        file_name="hello",
        class_name="Hello",
        date=date_str,
    )
    console.print("[bold cyan]Creating resources/hello.py file")

    touch_and_render(
        "orm/models.py",
        "model.py.jinja",
        file_name="models",
        separate_file=True,
        class_name="User",
        date=date_str,
    )
    console.print("[bold cyan]Creating orm/models.py file")
    
    with open("templates/base.html", "w+", encoding="utf-8") as base_html:
        base_html.write(
            PackageLoader("tulpar_cli").get_source(template_env, "base.html")[0]
        )
    console.print("[bold cyan]Creating templates/base.html file")
    
    with open("assets/htmx.min.js", "w+", encoding="utf-8") as htmx:
        htmx.write(requests.get("https://unpkg.com/htmx.org@1.7.0/dist/htmx.min.js").text)

    console.print("[bold cyan]Downloading htmx.min.js file")
    console.print(f"[bold blue]All done! {project_name} has been initialized!")
