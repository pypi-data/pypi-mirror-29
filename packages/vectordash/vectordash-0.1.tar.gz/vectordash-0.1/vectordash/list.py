import click
import requests
import json
import os

@click.command(name="list")



def list_machines():
    """Retrieves JSON object from vectordash using secret user token and displays the list of machines that the
       user is currently renting."""
    try:
        filename = "./vectordash_config/secret_token.txt"
        if os.path.isfile(filename):
            with open(filename) as f:
                secret_token = f.readline()
                full_url = "https://84119199.ngrok.io/api/list_machines/" + secret_token

            try:
                r = requests.get(full_url)

                if r.status_code == 200:
                    data = r.json()

                    for key, value in data.items():
                        machine = "[" + key + "]: " + value['name']
                        print(machine)
                else:
                    print("Could not connect to vectordash API with provided token")

            except json.decoder.JSONDecodeError:
                print("Invalid token value. Please make sure you are using the most recently generated token.")

        else:
            print("Please make sure a valid token is stored. Run 'vectordash secret <token>'")

    except TypeError:
        print("Please make sure a valid token is stored. Run 'vectordash secret <token>'")


# Run command line command vectordash list
if __name__ == '__main__':
    # When valid command is given (i.e no extra arguments)
    if len(sys.argv) == 1:
        list_machines()
    else:
        print("Incorrect number of arguments provided. Command should be of format 'vectordash list'")
