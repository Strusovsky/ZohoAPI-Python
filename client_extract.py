import requests
import pandas as pd
import datetime as dt
import json
from shutil import move


def get_acces_tk_from_refresh(refresh_token, client_configuration):
    """
    Function to request new access token by passing in refresh token
    Returns: New access token
    """
    try:
        config_file = open(client_configuration)
    except FileNotFoundError as e:
        print("The client_configuration.json file does not exist in the program directory.")
    else:
        client_configuration = json.load(config_file)
        refresh_url = 'https://accounts.zoho.com/oauth/v2/token'
        refresh_params = {
        "client_id":client_configuration["client_id"],
        "client_secret":client_configuration["client_secret"],
        "refresh_token":refresh_token,
        "grant_type":"refresh_token"
        }
        refresh_request = requests.post(refresh_url, refresh_params)
        refresh_status_json = refresh_request.json()
        return refresh_status_json["access_token"]


def make_request(field_string, page, module, access_token, refresh_token):
    """
    Function to make data extraction request to Zoho
    Return: JSON data file and request status
    """
    module_url = 'https://www.zohoapis.com/crm/v2/{}'.format(module)
    header = {'Authorization':'Zoho-oauthtoken {}'.format(access_token)}
    module_parameters = {'fields':field_string, 'page':page}
    module_request = requests.get(module_url, params=module_parameters, headers=header)
    module_request_status = module_request.status_code
    return module_request.json(), module_request_status


def get_all_module_records(module, field_string, token_file):
    """
    Function to get all records for specified Zoho module
    Return: Module JSON list
    """
    module_request_json_list = []
    with open(token_file) as data_file:
        access_response = json.load(data_file)
    access_token = access_response["access_token"]
    refresh_token = access_response["refresh_token"]
    not_end_of_module_records = True
    page = 1
    while not_end_of_module_records:
        module_request, module_request_status = make_request(field_string, page, module, access_token, refresh_token)
        print(module_request)
        print(module_request_status)
        if module_request_status != 200:
            access_token = get_acces_tk_from_refresh(refresh_token, "client_configuration.json")
            time = dt.datetime.now()
            print("Success: {} Refresh token obtained".format(time))
            continue
        module_request_json_list.append(module_request)
        page += 1
        not_end_of_module_records = module_request["info"]["more_records"]
    return module_request_json_list


def to_df(module_json_list):
    """
    Function to convert module json output into a Pandas DataFrame
    Return: Pandas DataFrame
    """
    module_data = pd.DataFrame()
    for array in module_json_list:
        for json_dict in array['data']:
            module_data = module_data.append(dict(json_dict), ignore_index=True)
    return module_data


def write_csv(module_data, file_name, dept):
    """
    Function to write module json output to csv via pandas dataframe
    Return: None
    """
    time = dt.datetime.now()
    filename = file_name + '-{}-{}-{}.csv'.format(time.day, time.hour, time.minute)
    module_data.to_csv(filename, encoding='utf-8')
    print('{} successfully written to Data/{} directory'.format(filename, dept))
    move("./{}".format(filename), "./Data/{}/{}".format(dept, filename))
