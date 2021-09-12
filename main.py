from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from Vsx import Vsx

app = FastAPI()

class Color(BaseModel):
    r: int
    g: int
    b: int

class Volume(BaseModel):
    raw: int
    percent: int

@app.post("/vsx/color")
def vsx_color( c: Color):
    print(c)
    vsx = Vsx()
    if c.r == 100 and c.g == 100 and c.b == 100:
        vsx.leiser()
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
