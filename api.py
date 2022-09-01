from fastapi import FastAPI
import joblib
# Creating FastAPI application
app = FastAPI()
# Import scheduler.py so we can modify the scheduler
from scheduler import app as app_rocketry
session = app_rocketry.session

def load_data(country,energy):
    cache_data= joblib.load('data/data'+country)
    cache_data['emissions'] = energy*cache_data['carbonIntensity']
    return cache_data

@app.get("/AR")
async def data_argentina(energy: int = 0):
    return load_data('AR',energy)

@app.get("/FR")
def data_francia(energy: int = 0):
    return load_data('FR',energy)

@app.get("/CL")
async def data_chile(energy: int = 0):
    return load_data('CL-SEN',energy)

@app.get("/BO")
async def data_bolivia(energy: int = 0):
    return load_data("BO",energy)

@app.get("/ZONES")
async def data_zonas():
    cache_data= joblib.load('data/zones')
    return cache_data

@app.get("/tasks")
async def read_tasks():
    return list(session.tasks)

@app.get("/logs")
async def read_logs():
    "Get task logs"
    repo = session.get_repo()
    return repo.filter_by().all()