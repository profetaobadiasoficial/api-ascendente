from fastapi import FastAPI
from skyfield.api import load, wgs84
from datetime import datetime
import os
import requests

app = FastAPI()

BSP_URL = "https://drive.google.com/uc?export=download&id=1CT2GSnQWAi8gFnqq5GN6vYkN-cdJBNGu"
BSP_PATH = "de431_part-2.bsp"

# Baixar o BSP se não existir
if not os.path.exists(BSP_PATH):
    print("Baixando arquivo BSP do Google Drive...")
    response = requests.get(BSP_URL)
    with open(BSP_PATH, "wb") as f:
        f.write(response.content)
    print("Download completo.")

planets = load(BSP_PATH)
earth = planets["earth"]

SIGNS = [
    "O Servo", "O Rei", "O Artesão", "O Guerreiro",
    "O Profeta", "O Sacerdote", "O Alegre", "O Irmão",
    "O Amado", "O Cordeiro", "O Peregrino", "O Sábio"
]

@app.get("/ascendente")
def calcular_ascendente(data: str, hora: str, lat: float, lon: float):
    dt_str = f"{data} {hora}"
    dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")

    ts = load.timescale()
    t = ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute)

    obs = earth + wgs84.latlon(latitude_degrees=lat, longitude_degrees=lon)
    astrometric = obs.at(t).observe(planets["sun"])
    apparent = astrometric.apparent()
    alt, az, distance = apparent.altaz()

    asc_degree = az.degrees
    signo_indice = int((asc_degree % 360) / 30)
    signo_nome = SIGNS[signo_indice]

    return {
        "ascendente": {
            "grau": round(asc_degree, 2),
            "indice": signo_indice,
            "signo": signo_nome
        }
    }

