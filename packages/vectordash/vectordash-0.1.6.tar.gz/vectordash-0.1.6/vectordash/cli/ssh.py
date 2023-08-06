import click
import requests
import json
import os
from colored import fg
from colored import stylize

from vectordash import API_URL, TOKEN_URL


@click.command()
@click.argument('machine', required=True, nargs=1)
def ssh(machine):
    """
    args: <machine>
    Runs an ssh command to the machine to allow user to connect.

    """
    try:
        # retrieve the secret token from the config folder
        root = str(os.path.expanduser("~"))
        token = root + "/.vectordash/token"

        if os.path.isfile(token):
            with open(token) as f:
                secret_token = f.readline()

            try:
                # API endpoint for machine information
                full_url = API_URL + str(secret_token)
                r = requests.get(full_url)

                # API connection is successful, retrieve the JSON object
                if r.status_code == 200:
                    data = r.json()

                    # machine provided is one this user has access to
                    if data.get(machine):
                        machine = (data.get(machine))
                        print(stylize("Machine exists. Connecting...", fg("green")))

                        # Machine pem
                        pem = machine['pem']

                        # name for pem key file, formatted to be stored
                        machine_name = (machine['name'].lower()).replace(" ", "")
                        key_file = root + "/.vectordash/" + machine_name + "-key.pem"

                        # create new file ~/.vectordash/<key_file>.pem to write into
                        with open(key_file, "w") as h:
                            h.write(pem)

                        # give key file permissions for ssh
                        os.system("chmod 600 " + key_file)

                        # Port, IP address, and user information for ssh command
                        port = str(machine['port'])
                        ip = str(machine['ip'])
                        user = str(machine['user'])

                        # execute ssh command
                        ssh_command = "ssh " + user + "@" + ip + " -p " + port + " -i " + key_file
                        print("Executing " + stylize(ssh_command, fg("blue")))
                        os.system(ssh_command)

                    else:
                        print(stylize(machine + " is not a valid machine id.", fg("red")))
                        print("Please make sure you are connecting to a valid machine")

                else:
                    print(stylize("Could not connect to vectordash API with provided token", fg("red")))

            except json.decoder.JSONDecodeError:
                print(stylize("Invalid token value", fg("red")))

        else:
            # If token is not stored, the command will not execute
            print(stylize("Unable to connect with stored token. Please make sure a valid token is stored.", fg("red")))
            print("Run " + stylize("vectordash secret <token>", fg("blue")))
            print("Your token can be found at " + stylize(str(TOKEN_URL), fg("blue")))

    except TypeError:
        type_err = "There was a problem with ssh. Please ensure your command is of the format "
        print(type_err + stylize("vectordash ssh <id>", fg("blue")))
