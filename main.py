from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()
# Definir un modelo de datos usando Pydantic
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

# Ruta POST que recibe un cuerpo JSON con los datos del modelo
@app.post("/items/")
def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price}


@app.get("/")

def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")

def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


