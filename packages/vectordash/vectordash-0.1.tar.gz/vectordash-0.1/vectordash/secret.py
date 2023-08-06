import click
import sys
import os


@click.command(name="secret")
@click.pass_context
# This dist function is needed for passing the context
def dist(ctx):
    ctx.invoke()


def store_secret(secret_token):
    """Stores the user's secret token."""
    try:
        filename = "./vectordash_config/secret_token.txt"
        # if a previous token was stored, update it
        if os.path.isdir("./vectordash_config") and os.path.isfile(filename):

            # retrieve previous token (this may be unnecessary)
            with open(filename) as f:
                lines = f.readlines()

            # change to user's new provided token
            lines[0] = secret_token

            # update file with new token
            with open(filename, "w") as g:
                g.writelines(lines)

            print("Secret token changed and stored.")

        else:
            if not os.path.isdir("./vectordash_config"):
                os.system("mkdir ./vectordash_config")

                print("Made directory ./vectordash_config")

            # create new file ./secret_token to write into and add the secret token
            with open(filename, "w") as h:
                h.write(secret_token)

            print("Secret token created and stored.")

    except TypeError:
        print("Please make sure you are using the most recently generated token.")

# Run command line command vectordash secret <token>
if __name__ == '__main__':
    # When valid command is given (i.e ONE token is provided)
    if len(sys.argv) == 2:

        # Retrieve secret token from command and store it
        secret_token = sys.argv[1]
        store_secret(secret_token)
    else:
        print("Incorrect number of arguments provided. Command should be of format 'vectordash secret <token>'")
