import click
import requests
import json
import os
from colored import fg
from colored import stylize
from colored import attr

from vectordash import API_URL, TOKEN_URL

@click.command()
def list():
    """
    args: None
    Displays the list of machines that user is currently renting

    """
    try:
        filename = os.path.expanduser('~/.vectordash/token')

        if os.path.isfile(filename):
            with open(filename) as f:
                secret_token = f.readline()
                full_url = API_URL + str(secret_token)

            try:
                r = requests.get(full_url)

                if r.status_code == 200:
                    data = r.json()

                    if len(data) > 0:
                        green_bolded = fg("green") + attr("bold")
                        print("Your Vectordash machines:")
                        for key, value in data.items():
                            pretty_id = stylize("[" + str(key) + "]", green_bolded)
                            machine = str(pretty_id) + " " + str(value['name'])
                            print(machine)
                    else:
                        vd = stylize("https://vectordash.com", fg("blue"))
                        print("You are not currently renting any machine. Go to " + vd + " to browse GPUs.")
                else:
                    print(stylize("Could not connect to vectordash API with provided token", fg("red")))

            except json.decoder.JSONDecodeError:
                print(stylize("Invalid token value", fg("red")))

        else:
            print(stylize("Unable to locate token. Please make sure a valid token is stored.", fg("red")))
            print("Run " + stylize("vectordash secret <token>", fg("blue")))
            print("Your token can be found at " + stylize(str(TOKEN_URL), fg("blue")))

    except TypeError:
        type_err = "Please make sure a valid token is stored. Run "
        print(type_err + stylize("vectordash secret <token>", fg("blue")))
