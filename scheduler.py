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
            output_data = {}
            
            output_data = process_data(data)
            joblib.dump(output_data , 'data/data'+country)
# Creating some tasks

def process_data(data):
    processed_data = {}
    renewable_share= 100 - data['data']['fossilFuelPercentage']
    if renewable_share <= 20:
            processed_data['name'] = 'Dependiendo de combustibles fósiles'
            processed_data['description'] = "Usamos un porcentaje de energía renovable menor al 20%, estamos en proceso de mejorar nuestra huella de carbono con proyectos para consumir energía de fuentes renovables"
            processed_data['image'] = 'https://github.com/LuisFDuarte/SelloChainedCO2API/raw/main/images/fossil.jpg'
              
    if renewable_share > 20 and renewable_share <=50:
            processed_data['name'] = 'Empezando la transición energética'
            processed_data['description'] = "Usamos un porcentaje de energía renovable menor al 50%, estamos en camino de la transición energética para mejorar nuestra huella de carbono en nuestros productos o servicios."
            processed_data['image'] = 'https://github.com/LuisFDuarte/SelloChainedCO2API/raw/main/images/greenmobility.jpg'
            
    if renewable_share > 50 and renewable_share <=80:
            processed_data['name'] = 'Desarrollando la transición energética'
            processed_data['description'] = "Usamos un porcentaje de energía renovable mayor al 50%, estamos activamente desarrollando nuestra transición energética para mejorar nuestra huella de carbono."
            processed_data['image'] = 'https://github.com/LuisFDuarte/SelloChainedCO2API/raw/main/images/sustainableEnergy.jpg'
            
    if renewable_share > 80 and renewable_share <=100:
            processed_data['name'] = 'Construimos productos y servicios con fuentes renovables'
            processed_data['description'] = "Usamos un porcentaje de energía renovable mayor al 80%, estamos comprometidos con el uso de energías renovables para reducir  la huella de carbono de nuestros productos y servicios."
            processed_data['image'] = 'https://github.com/LuisFDuarte/SelloChainedCO2API/raw/main/images/sustainableHouses.jpg'
           
    processed_data['attributes'] = [
                {
                    'trait_type': 'Energía renovable %',
                    'value': renewable_share
                },
                {
                    'trait_type': 'Intensidad de carbono gCO2/kWh', 
                    'value': data['data']['carbonIntensity']
                },
                {
                    'trait_type': 'País', 
                    'value': data['countryCode']
                } 
    ]

    processed_data['datetime'] = data['data']['datetime']
    processed_data['_disclaimer'] = data['_disclaimer']
    return processed_data

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