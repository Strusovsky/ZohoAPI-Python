import requests
import json


def get_access_token(client_configuration):
    """
    Function to a request access token from the Zoho API
    Output: writes request response to json in program directory
    """
    try:
        config_file = open(client_configuration)
    except FileNotFoundError as e:
        print("The client_configuration.json file does not exist in the program directory.")
    else:
        client_configuration = json.load(config_file)
        access_params = {
        'client_id':client_configuration["client_id"],
        'client_secret':client_configuration["client_secret"],
        'redirect_uri':client_configuration["redirect_uri"],
        'code':client_configuration["grant_code"],
        'grant_type':"authorization_code",
        'access_type':"offline"
        }
        access_url = 'https://accounts.zoho.com/oauth/v2/token'
        access_request = requests.post(access_url, access_params)
        access_request_json = access_request.json()
        with open("client_access_response.json", "w") as outfile:
            json.dump(access_request_json, outfile, indent=4)
