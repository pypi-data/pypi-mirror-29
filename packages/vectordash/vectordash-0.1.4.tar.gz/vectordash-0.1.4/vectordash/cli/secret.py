import click
import os
from colored import fg
from colored import stylize


@click.command()
@click.argument('token', required=True, nargs=1)
def secret(token):
    """
    Stores the user's secret token

    """
    try:
        root = str(os.path.expanduser("~"))
        filename = root + "/.vectordash/token"
        # if a previous token was stored, update it
        if os.path.isdir(root + "/.vectordash") and os.path.isfile(filename):

            # retrieve previous token (this may be unnecessary)
            with open(filename) as f:
                lines = f.readlines()

            # change to user's new provided token
            lines[0] = token

            # update file with new token
            with open(filename, "w") as g:
                g.writelines(lines)

            print(stylize("Secret token changed and stored.", fg("green")))

        else:
            if not os.path.isdir(root + "/.vectordash"):
                cmd = "mkdir " + root + "/.vectordash"
                os.system(cmd)

                print(stylize("Made directory ~/.vectordash", fg("green")))

            # create new file ~/.vectordash/token to write into and add the secret token
            with open(filename, "w") as h:
                h.write(token)

            print(stylize("Secret token created and stored.", fg("green")))

    except TypeError:
        print(stylize("Please make sure you are using the most recently generated token.", fg("red")))
