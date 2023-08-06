import click

from vectordash.cli.list import list
from vectordash.cli.secret import secret
from vectordash.cli.ssh import ssh
from vectordash.cli.pull import pull
from vectordash.cli.push import push


@click.group()
def cli():
    """
    Vectordash CLI interacts with Vectordash server and executes your commands.
    More help is available under each command listed below.
    """
    pass


def add_commands(cli):
    cli.add_command(list)
    cli.add_command(secret)
    cli.add_command(ssh)
    cli.add_command(push)
    cli.add_command(pull)


add_commands(cli)
