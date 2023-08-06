import click
import os
from colored import fg
from colored import stylize


@click.command()
@click.argument('token', required=True, nargs=1)
def secret(token):
    """
    args: <token>
    Stores the user's secret token

    """
    try:
        # defining the dot folder path and token file name
        dot_folder = os.path.expanduser('~/.vectordash')
        token_path = os.path.join(dot_folder, 'token')

        # ensuring ~/.vectordash/ exists
        if not os.path.isdir(dot_folder):
            os.mkdir(dot_folder)

        # writing out the token
        with open(token_path, 'w') as f:
            f.write(str(token))

        print(stylize("Secret successfully updated.", fg("green")))

    except TypeError:
        print(stylize("Error: the provided token was an invalid type.", fg("red")))
