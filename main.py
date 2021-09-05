from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import subprocess, imp

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None
        
class Volume(BaseModel):
    raw: int
    percent: int
        

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.post("/items")
def update_item( item: Item):
    print(item)
    return {"item_name": item.name, "item_id": "2"}

@app.post("/vsx/volume")
def vsx_volume( vol: Volume):
    print(vol)
    v = imp.load_source("habridge.vsx", "/home/pi/habridge/skripte/vsx.py")
    vsx = v.VSX()
    vsx.volume(vol.raw)
    return {"item_id": "2"}

@app.get("/vsx/on")
def vsx_on():
    v = imp.load_source("habridge.vsx", "/home/pi/habridge/skripte/vsx.py")
    vsx = v.VSX()
    vsx.einschalten()
    return {}


@app.get("/vsx/off")
def vsx_off():
    v = imp.load_source("habridge.vsx", "/home/pi/habridge/skripte/vsx.py")
    vsx = v.VSX()
    vsx.ausschalten()
    return {}
