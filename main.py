from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from Vsx import Vsx

app = FastAPI()
        
class Volume(BaseModel):
    raw: int
    percent: int

@app.post("/vsx/leiser")
def vsx_volume( vol: Volume):
    vsx = Vsx()
    vsx.leiser(vol.percent)
    return {}

@app.post("/vsx/volume")
def vsx_volume( vol: Volume):
    vsx = Vsx()
    vsx.volume(vol.percent)
    return {}

@app.get("/vsx/on")
def vsx_on():
    vsx = Vsx()
    vsx.einschalten()
    return {}

@app.get("/vsx/off")
def vsx_off():
    vsx = Vsx()
    vsx.ausschalten()
    return {}
