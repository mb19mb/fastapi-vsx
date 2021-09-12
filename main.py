from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import subprocess, imp
from VsxTelnetClient import VsxTelnetClient

app = FastAPI()
        
class Volume(BaseModel):
    raw: int
    percent: int
        
def log(msg):
    f = file.open("/tmp/vsx.log", "aw")
    f.write(msg+"\n")
    f.close()

@app.post("/vsx/volume")
def vsx_volume( vol: Volume):
    log("fast-api volume")
    log(vol)
    v = imp.load_source("habridge.vsx", "/home/pi/habridge/skripte/vsx.py")
    vsx = v.VSX()
    vsx.volume(vol.percent)
    return {}

@app.get("/vsx/on")
def vsx_on():
    #v = imp.load_source("habridge.vsx", "/home/pi/habridge/skripte/vsx.py")
    #vsx = v.VSX()
    #vsx.einschalten()
    vsx = Vsx()
    vsx.einschalten()
    return {}


@app.get("/vsx/off")
def vsx_off():
    log("fast-api off")
    v = imp.load_source("habridge.vsx", "/home/pi/habridge/skripte/vsx.py")
    vsx = v.VSX()
    vsx.ausschalten()
    return {}

@app.get("/")
def read_root():
    return {"Hello": "World"}
