import click
from flask.cli import FlaskGroup

from data_decoupling_automation.commands import examples  # noqa: E402


def create_app_wrapper():
    from data_decoupling_automation.app import create_app

    return create_app()


# This will create the instance of the of the Flask application and
# makes it accessible with flask.current_app.
@click.group(cls=FlaskGroup, create_app=create_app_wrapper)
def cli():
    """This is a management script for data-decoupling-automation"""


@cli.command()
def log_hello_world():
    """
    Example command, prints hello world to stdout
    """
    examples.log_hello_world()


if __name__ == "__main__":
    cli()
