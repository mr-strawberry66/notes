"""Wrapper around Notes CLI."""
import os
from commands.notes import delete, find, ls, new, update

import click
import pyfiglet


@click.group()
def cli():
    """Group for Notes CLI."""


@cli.command()
def version():
    """Display version information."""
    text = pyfiglet.figlet_format("Notes", font="slant")
    click.echo(text)
    click.echo(f"Version: {_version()}")


def _version():
    """Read version file for the module."""
    pathname = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__), "version.txt")
    )

    with open(pathname, "r") as f:
        return f.read()


cli.add_command(cmd=delete, name="delete")
cli.add_command(cmd=find, name="find")
cli.add_command(cmd=ls, name="ls")
cli.add_command(cmd=new, name="new")
cli.add_command(cmd=update, name="update")
