from fastapi import FastAPI, Query
from pydantic import BaseModel
from skyfield.api import load, Topos
from datetime import datetime
import math

app = FastAPI()

# Carrega efemérides
ephemeris = load('de431t.bsp')  # Você pode usar o de431_part-2.bsp também
earth = ephemeris['earth']
sun = ephemeris['sun']

# Signos fixos em graus (30° cada, começando em 0°)
signos = [
    "O Servo", "O Rei", "O Artesão", "O Guerreiro",
    "O Profeta", "O Sacerdote", "O Alegre", "O Irmão",
    "O Amado", "O Cordeiro", "O Peregrino", "O Sábio"
]

@app.get("/ascendente")
def calcular_ascendente(
    data: str = Query(..., description="Formato: YYYY-MM-DD"),
    hora: str = Query(..., description="Formato: HH:MM"),
    lat: float = Query(...),
    lon: float = Query(...)
):
    ts = load.timescale()
    dt = datetime.strptime(f"{data} {hora}", "%Y-%m-%d %H:%M")
    t = ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute)

    observador = earth + Topos(latitude_degrees=lat, longitude_degrees=lon)
    astrometrico = observador.at(t).observe(sun).apparent()
    ra, dec, _ = astrometrico.radec()

    grau = ra.hours * 15  # 24h = 360°
    indice = int(grau // 30) % 12
    signo = signos[indice]

    return {
        "ascendente": {
            "grau": round(grau, 2),
            "indice": indice,
            "signo": signo
        }
    }
