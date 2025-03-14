"""Command Line Interface for UPE engineer's IT Division security lock manager system"""

import pkg_resources
import rich_click as click
from rich.console import Console
from rich.table import Table

from division import core
from division.utils.constraints import DATEFMT
from division.models.constraints import AccessKeyType

click.rich_click.USE_RICH_MARKUP = True
click.rich_click.USE_MARKDOWN = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.SHOW_METAVARS_COLUMN = False
click.rich_click.APPEND_METAVARS_HELP = True


@click.group()
@click.version_option(pkg_resources.get_distribution("division").version)
def main():
    """Command Line Interface for UPE engineer's IT Division security lock manager system"""


@main.command()
def start():
    core.watch_dog()


@main.command()
def init():
    core.init_db()


@main.command()
@click.argument("value", type=click.STRING)
@click.option("--type", default=AccessKeyType.PASSWORD, type=AccessKeyType)
def validate(**kargs):
    """Validate a given key..."""
    console = Console()
    try:
        key = core.validate_key(**kargs)
        table = Table()
        table.add_column("User")
        table.add_column("Role")
        table.add_column("Type")
        table.add_column("Expiration")

        table.add_row(
            key.user.name,
            key.user.role.name,
            key.type.value,
            key.expiration.strftime(DATEFMT),
        )

        console.print(table)
    except Exception:
        console.print_exception()
