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
    Displays the list of machines that user is currently renting

    """
    try:
        filename = "./vectordash_config/token.txt"
        if os.path.isfile(filename):
            with open(filename) as f:
                token = f.readline()
                full_url = API_URL + str(token)

            try:
                r = requests.get(full_url)

                if r.status_code == 200:
                    data = r.json()

                    if len(data) > 0:
                        print("Your Vectordash machines:")
                        for key, value in data.items():
                            green_bolded = fg("green") + attr("bold")
                            pretty_id = stylize("[" + str(key) + "]", green_bolded)
                            machine = str(pretty_id) + " " + str(value['name'])
                            print(machine)
                    else:
                        print("You are not currently renting any machine. Go to https://vectordash.com to browse GPUs.")
                else:
                    print(stylize("Could not connect to vectordash API with provided token", fg("red")))

            except json.decoder.JSONDecodeError:
                print(stylize("Invalid token value", fg("red")))

        else:
            print("Unable to locate token. Please make sure a valid token is stored.")
            print("Run " + stylize("vectordash secret <token>", fg("blue")))
            print("Your token can be found at " + stylize(str(TOKEN_URL), fg("blue")))

    except TypeError:
        type_err = "Please make sure a valid token is stored. Run "
        print(type_err + stylize("vectordash secret <token>", fg("blue")))
