# ZohoAPI-Python
A Python program to authorise your client application, schedule and extract Zoho CRM module data.

#### Running the program

The program runs by reading off configuration files and a client request response file.

* Simply, add your client credentials to `client_configuration.json`:

```
{
    "client_id":"client_id_goes_here",
    "client_secret":"client_secret_goes_here",
    "grant_code":"grant_code_goes_here",
    "redirect_uri":"redirect_uri_goes_here"
}
```

* Add the module name and a comma separated string of API field names you wish to extract to `client_module_configuration.json`:

```
{
    "Contacts":"api_field_1,api_field_2",
    "Leads":"api_field_1,api_field_2"
}
```

* Open up a command line shell in the program directory and run:

```
>> python run.py
```

The extraction file will get saved into either the program directory or a directory of your choice. See the `run.py` source file for more information on this.

#### Amending the extract schedule

To amend the extraction rate, go into the `run.py` file and amend the following code:
```
value = 10 # Amend value
schedule.every(value).minutes.do(extract)
while True:
    schedule.run_pending()
    time.sleep(1)
```

The code defaults to request data every 10 mins.

#### Improvements

This program was used while I worked on a dashboard application to display sales and on-boarding data. There are a lot of further improvements that can be done to these scripts, so feel free to clone this repository and improve the base source code.
