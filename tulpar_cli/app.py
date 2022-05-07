"""
tulpar_cli/app.py
Ian Kollipara
2022.04.05

Main CLI file
"""

# Imports
from typer import Typer
from .generate import generate
from .manage import manage

tulpar = Typer(
    help="""
Tulpar CLI Tool

Tulpar is a Python SSR Framework built on top of Falcon, PonyORM,
Jinja2, and HTMX. Tulpar only supports HATEOAS as the mode of
communication between frontend and backend.
"""
)

from .new import new_project

tulpar.add_typer(generate, name="generate", short_help="Generate new components")
tulpar.add_typer(manage, name="manage", short_help="Manage Tulpar project")
