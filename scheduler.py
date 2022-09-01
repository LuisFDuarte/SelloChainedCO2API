from rocketry import Rocketry
from rocketry.conds import every, after_success
import requests
from requests.exceptions import HTTPError
from requests.exceptions import Timeout
import joblib
from dotenv import load_dotenv
import os

load_dotenv('keys.env')
TOKEN_CO2 = str(os.getenv('TOKEN_CO2'))
COUNTRIES = str(os.getenv('COUNTRIES'))

# Creating the Rocketry app
app = Rocketry(config={"task_execution": "async"})

def data_zones():
    url = "https://api.electricitymap.org/v3/zones"
    try:
        response = requests.request("GET", url, timeout=3)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Timeout as err:
        print(f'The request timed out: {err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        data=response.json()
        joblib.dump(data , 'data/zones')
    
def data_from_country(country):
    url = "https://api.co2signal.com/v1/latest"
    querystring = {"countryCode":country}
    headers = {
        'auth-token': TOKEN_CO2,
        # 'cache-control': "no-cache",
        }
    try:
        response = requests.request("GET", 
                                    url, 
                                    headers=headers, 
                                    params=querystring,
                                    timeout=3)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Timeout as err:
        print(f'The request timed out: {err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        data=response.json()
        if "data" in data:
            filtered_data = {}
            filtered_data['country'] = data['countryCode']
            filtered_data['datetime'] = data['data']['datetime']
            filtered_data['carbonIntensity'] = data['data']['carbonIntensity']
            filtered_data['fossilFuelPercentage'] = data['data']['fossilFuelPercentage']
            filtered_data['_disclaimer'] = data['_disclaimer']
            joblib.dump(filtered_data , 'data/data'+country)
# Creating some tasks

@app.task('daily')
async def do_daily():
    data_zones()

@app.task('every 1 hour')
async def do_requests():
    countries = COUNTRIES.split(",")
    for country in countries:
        print("Doing a task for "+country)
        data_from_country(country)

# @app.task(after_success(do_requests))
# async def do_after():
#     print("Task Done")

if __name__ == "__main__":
    # If this script is run, only Rocketry is run
    app.run()