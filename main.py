from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from Vsx import Vsx

app = FastAPI()

class Color(BaseModel):
    r: int
    g: int
    b: int
    h: int

class Volume(BaseModel):
    raw: int
    percent: int

@app.post("/vsx/color")
def vsx_color( c: Color):
    print(c)
    vsx = Vsx()
    if c.h == 21845: #c.r == 255 and c.g == 2 and c.b == 2: # ROT
        vsx.leiser()
    if c.h == 43690: #c.r == 102 and c.g == 102 and c.b == 255: # BLAU
        vsx.lauter()
    if c.h == 3095:
        vsx.umschalten("CD")
    if c.h == 7100:
        vsx.umschalten("PS3")
    if c.h == 100:
        vsx.umschalten("TV")
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
