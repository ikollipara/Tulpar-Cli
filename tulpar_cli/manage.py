"""
tulpar_cli/manage.py
Ian Kollipara
2022.04.05

Manage Command Group
"""
# Imports
from importlib.util import find_spec
from subprocess import run

from rich import get_console
from typer import Argument, Exit, Option, Typer

# Initialize the Typer Command Group
# and the rich console for output
console = get_console()
manage = Typer(
    help="""

Manage your Tulpar project through these utility commands.
Each one simplifies the commands that one would have to run.

"""
)


def find_or_raise(mod_name: str) -> None:
    """Exit the Cli if the module doesn't exist.

    Used internally for handling the existence of the
    CLI tools used.
    """

    if find_spec(mod_name) is None:
        console.print(f"[bold red]Please install {mod_name}")
        raise Exit(1)


@manage.command("lint")
def lint(
    file_path: str = Argument(".", help="File/Directory to lint", metavar="PATH"),
    dry_run: bool = Option(False, "--dry-run", help="Do Output, but do not run"),
):
    """Lint your Application.

    Tulpar uses Pylint to lint an application. You can specify the file path.
    """

    find_or_raise("pylint")

    if not dry_run:

        console.print(
            run(
                ["pylint", file_path], check=False, shell=False, capture_output=True
            ).stdout
        )

    console.print(f"[bold blue] {file_path} was linted with pylint")


@manage.command("format")
def tulpar_format(
    file_path: str = Argument(".", help="File/Directory to format", metavar="PATH"),
    dry_run: bool = Option(
        False, "--dry-run", help="Show output, but don't do any actual formatting"
    ),
):
    """Format your Application.

    Tulpar uses Black and isort to format your codebase. You can specify the file path.
    """

    find_or_raise("black")
    find_or_raise("isort")

    if not dry_run:

        console.print(
            run(
                ["black", file_path], check=False, capture_output=True, shell=False
            ).stdout
        )
        console.print(
            run(
                ["isort", file_path], check=False, capture_output=True, shell=False
            ).stdout
        )

    console.print(f"[bold blue] {file_path} was formatted with Black and Isort")


@manage.command("test")
def test():
    """Test your application.

    Tulpar uses Pytest to do application testing. You can still use Unittests and NoseTests,
    as pytest handles those as well. Pytest is ran with the verbose flag on.
    """

    find_or_raise("pytest")

    console.print(
        run(
            ["pytest", "--verbose"], shell=False, check=False, capture_output=True
        ).stdout
    )


@manage.command("audit")
def audit(
    file_path: str = Argument(".", help="File/Directory to audit", metavar="PATH")
):
    """Audit your Application.

    Tulpar uses Bandit to audit your application.
    """

    find_or_raise("bandit")

    console.print(
        run(["bandit", file_path], shell=False, check=False, capture_output=True).stdout
    )
