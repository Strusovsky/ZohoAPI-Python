import json
import datetime as dt
from client_extract import get_all_module_records
from client_extract import make_request
from client_extract import get_acces_tk_from_refresh
from client_authorise import get_access_token
from client_extract import to_df
from client_extract import write_csv
import schedule
import time


def main():

    def access_token_validation():
        """
        Function to request access token
        Return: Boolean value determining call success / failure
        """
        try:
            client_tokens = open("client_access_response.json")
        except FileNotFoundError:
            status_code = get_access_token("client_configuration.json")
        else:
            client_configuration = json.load(client_tokens)
            for key in client_configuration.keys():
                time = dt.datetime.now()
                if key == "access_token":
                    success_str = "Access and refresh tokens obtained successfully"
                    success_msg = "Success: {} {}".format(time, success_str)
                    print(success_msg)
                    return True
                else:
                    method = "get_access_token()"
                    error_str = "\nThere's been an error in getting your access token. Try checking your grant_code."
                    error_msg = "Error: {} {}-{}-{} {}".format(method, time.day, time.hour, time.minute, error_str)
                    print(error_msg)
                    return False


    def get_module_data(module, access_from_grant_tk, file_name, dept):
        """
        Function to extract Zoho CRM module data
        Return: None - data is written to file
        """
        if access_from_grant_tk:
            try:
                module_config = open("client_module_configuration.json")
            except FileNotFoundError:
                print("There's no client_module_configuration file in the working directory")
            else:
                client_module_configuration = json.load(module_config)
                token_file = "client_access_response.json"
                contacts_data = get_all_module_records(module, client_module_configuration[module], token_file)
                write_csv(to_df(contacts_data), file_name, dept)


    def extract():
        """
        Function to call get_module_data within scheduling code
        Note: multiple calls to get_module_data can be done within
              this function for various Zoho modules
        """
        get_module_data("Module", access_from_grant_tk, "file_name_example", "output_folder_example")


    # Access token call
    access_from_grant_tk = access_token_validation()

    # Scheduling code
    value = 10
    schedule.every(value).minutes.do(extract) # Extract data from Zoho
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
