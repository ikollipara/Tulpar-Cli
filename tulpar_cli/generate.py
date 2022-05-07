"""
tulpar_cli/generate.py
Ian Kollipara
2022.04.05

Generate Command Group
"""

# Imports
from datetime import date
from os.path import exists

from rich import get_console
from typer import Argument, Exit, Option, Typer

from .utils import template_env

generate = Typer(
    help="""

Generate new components for Tulpar Project. These
are automatically added to their correct folders,
setup up to be automatically running.

"""
)
console = get_console()


def exists_or_raise(dirname: str) -> None:
    """Check if a directory exists.

    Given a directory name, check if it exists,
    if not raise an Exit.
    """

    if not exists(dirname):
        console.print(f"[bold red]no '{dirname}' directory found!")
        raise Exit(1)


@generate.command("page")
def gen_page(
    name: str = Argument(..., help="Name of the Page"),
    dry_run: bool = Option(
        False, "--dry-run", help="Show output, but don't modify anything"
    ),
):
    """Generate a Page

    Generate a page with the given name. The file will exist within
    the Pages directory, and have the name provided. The main function within
    the page must have the same name as the module and be decorated with @Page().
    """

    exists_or_raise("pages")

    date_str = date.today().strftime("%Y.%m.%d")

    new_page_file = template_env.get_template("page.py.jinja").render(
        file_name=name, date=date_str
    )

    if not dry_run:
        with open(f"pages/{name}.py", "w+", encoding="utf-8") as new_page:
            new_page.write(new_page_file)

    console.print(f"[bold blue] pages/{name}.py has been created!")


@generate.command("resource")
def gen_resource(
    name: str = Argument(..., help="Name of the Resource"),
    dry_run: bool = Option(
        False, "--dry-run", help="Show output, but don't modify anything"
    ),
):
    """Generate a Resource

    Generate a resource with the given name. The file will exist within the Resources directory,
    and have a CamelCase name of the string provided. The class will be decorated with a
    @Resource, and must have an on_* method defined (see Falcon documentation).
    """

    exists_or_raise("resources")

    date_str = date.today().strftime("%Y.%m.%d")
    class_name = "".join(map(str.capitalize, name.split("_")))

    new_resource_file = template_env.get_template("resources.py.jinja").render(
        file_name=name, date=date_str, class_name=class_name
    )

    if not dry_run:
        with open(f"resources/{name}.py", "w+", encoding="utf-8") as new_resource:
            new_resource.write(new_resource_file)

    console.print(f"[bold blue] resources/{name}.py has been created!")


@generate.command("middleware")
def gen_middleware(
    name: str = Argument(..., help="Name of the Middleware"),
    dry_run: bool = Option(
        False, "--dry-run", help="Show output, but don't modify anything"
    ),
):
    """Generate a Middleware

    Generate a middleware with the given name. The file will exist within the Middleware directory,
    and have a CamelCase + Middleware name of the string provided. The class will inherit from
    TulparMiddleware, and must implement all methods of the base class.
    """

    exists_or_raise("middleware")

    date_str = date.today().strftime("%Y.%m.%d")
    class_name = "".join(map(str.capitalize, name.split("_")))

    new_middleware_file = template_env.get_template("middleware.py.jinja").render(
        file_name=name, date=date_str, class_name=class_name
    )

    if not dry_run:
        with open(f"middleware/{name}.py", "w+", encoding="utf-8") as new_middleware:
            new_middleware.write(new_middleware_file)

    console.print(f"[bold blue] middleware/{name}.py has been created!")


@generate.command("hook")
def gen_hook(
    name: str = Argument(..., help="Name of the Hook"),
    dry_run: bool = Option(
        False, "--dry-run", help="Show output, but don't modify anything"
    ),
    as_class: bool = Option(
        False, "--as-class", "-c", help="Initialize the hook as a class"
    ),
):
    """Generate a Hook

    Generate a hook with the given name. The file will exist within the Hooks directory,
    and have a CamelCase name of the string provided. The hook may be initialized as a function
    or as a class, both of which must conform to the Tulpar hook protocol (see Falcon hook for
    details).
    """

    exists_or_raise("hooks")

    date_str = date.today().strftime("%Y.%m.%d")
    class_name = "".join(map(str.capitalize, name.split("_")))

    new_hook_file = template_env.get_template("hook.py.jinja").render(
        file_name=name, date=date_str, class_name=class_name, as_class=as_class
    )

    if not dry_run:
        with open(f"hooks/{name}.py", "w+", encoding="utf-8") as new_hook:
            new_hook.write(new_hook_file)

    console.print(f"[bold blue] hooks/{name}.py has been created!")


@generate.command("model")
def gen_model(
    name: str = Argument(..., help="Name of the Hook"),
    dry_run: bool = Option(
        False, "--dry-run", help="Show output, but don't modify anything"
    ),
    separate_file: bool = Option(
        False, "--separate-file", "-s", help="Generate the model on a separate file"
    ),
):
    """Generate a PonyORM Model

    Generate a PonyORM model with the specified name. The model will exist within the ORM
    directory, and have a CamelCase name of the string provided. The model may be initialized
    as a separate file or on the models.py file. The default behavior is on the models.py file.
    (See PonyORM documentation for more detail).
    """

    exists_or_raise("orm")

    date_str = date.today().strftime("%Y.%m.%d")
    class_name = "".join(map(str.capitalize, name.split("_")))

    new_model_file = template_env.get_template("model.py.jinja").render(
        file_name=name,
        date=date_str,
        class_name=class_name,
        separate_file=separate_file,
    )

    filename = name if separate_file else "models"
    mode = "w+" if separate_file else "a+"

    if not dry_run:
        with open(f"orm/{filename}.py", mode, encoding="utf-8") as new_model:
            new_model.write(new_model_file)

    console.print(
        f"[bold blue] orm/{filename}.py has been {'added' if separate_file else 'created'}!"
    )
