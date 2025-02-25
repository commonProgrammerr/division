"""Command Line Interface for UPE engineer's IT Division security lock manager system"""

import pkg_resources
import rich_click as click
from rich.console import Console
from rich.table import Table

from division import core
from division.config.settings import DATEFMT
from division.models import AccessKeyType

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
@click.argument("key", type=click.STRING)
@click.option("--type", default=AccessKeyType.PASSWORD, type=AccessKeyType)
def validate(key, type):
    """Validate a given key..."""
    console = Console()
    try:
        key = core.validate_access_key(key_type=type, key_value=key)
        table = Table()
        table.add_column("User")
        table.add_column("Type")
        table.add_column("Expiration")

        table.add_row(
            key.user.name,
            key.type.value,
            key.expiration.strftime(DATEFMT),
        )

        console.print(table)
    except RuntimeError:
        console.print_exception()
