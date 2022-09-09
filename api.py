from fileinput import filename
import joblib
import aiofiles
from fastapi import FastAPI, File, UploadFile,Form
import os
from os.path import isfile, join
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost:3001",
    "http://localhost",
    "http://localhost:3000",
    "https://luisfduarte.github.io/SelloChainedCO2Interface/",
    'https://luisfduarte.github.io'
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Import scheduler.py so we can modify the scheduler
from scheduler import app as app_rocketry
session = app_rocketry.session

def load_data(country,energy):
    cache_data= joblib.load('data/data'+country)
    cache_data['attributes'].append({
        'trait_type': 'Emisiones gCO2',
        'value': energy*cache_data['attributes'][1]['value']})
    return cache_data

@app.get("/AR")
async def data_argentina(energy: int = 0):
    return load_data('AR',energy)

@app.get("/AW")
async def data_aruba(energy: int = 0):
    return load_data("AW",energy)

@app.get("/BO")
async def data_bolivia(energy: int = 0):
    return load_data("BO",energy)

# @app.get("/BB")
# async def data_barbados(energy: int = 0):
#     return load_data("BB",energy)

# @app.get("/BZ")
# async def data_belice(energy: int = 0):
#     return load_data("BZ",energy)

# @app.get("/BS")
# async def data_bahamas(energy: int = 0):
#     return load_data("BS",energy)

# @app.get("/CO")
# async def data_colombia(energy: int = 0):
#     return load_data("CO",energy)

@app.get("/CL")
async def data_chile(energy: int = 0):
    return load_data('CL-SEN',energy)

@app.get("/CR")
async def data_costa_rica(energy: int = 0):
    return load_data("CR",energy)

@app.get("/DO")
async def data_republica_dominica(energy: int = 0):
    return load_data("DO",energy)

@app.get("/FR")
def data_francia(energy: int = 0):
    return load_data('FR',energy)

@app.get("/GT")
async def data_guatemala(energy: int = 0):
    return load_data("GT",energy)

@app.get("/HN")
async def data_honduras(energy: int = 0):
    return load_data("HN",energy)

@app.get("/IS")
async def data_islandia(energy: int = 0):
    return load_data("IS",energy)

@app.get("/NI")
async def data_nicaragua(energy: int = 0):
    return load_data("NI",energy)

@app.get("/PE")
async def data_peru(energy: int = 0):
    return load_data("PE",energy)

@app.get("/SV")
async def data_elsalvador(energy: int = 0):
    return load_data("SV",energy)

@app.get("/UY")
async def data_uruguay(energy: int = 0):
    return load_data("UY",energy)


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

@app.post("/uploadFile/")

async def post_endpoint(user: str = Form(...),in_file: UploadFile=File(...)):
    print(user)
    filename = './uploadedFiles/'+user+'/'+str(in_file.filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    async with aiofiles.open(filename, 'wb') as out_file:
        while content := await in_file.read(1024):  # async read chunk
            await out_file.write(content)  # async write chunk

    return {"Resultado": "Archivo Subido"}

@app.get("/paths/")
async  def get_items():
    results={}
    mypath='uploadedFiles'
    onlyfiles = []
    for path, currentDirectory, files in os.walk(mypath):
        for file in files:
            onlyfiles.append(join(path, file))
    
    results["folders"] = [
        val for val in onlyfiles]
    print(onlyfiles)
    return results

@app.get("/download/")
async def get_file(p: str= ''):
    head, tail = os.path.split(p)
    return FileResponse(p, media_type='application/octet-stream',filename=tail)