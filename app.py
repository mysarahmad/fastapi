from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel,Field
from typing import Optional,List

app = FastAPI()

class Profile(BaseModel):
    name : str
    age : Optional[int] = None

class Product(BaseModel):
    name : str = Field(title="name which you want to give",
                       description="provide your name only")
    price : int
    discount : int
    discounted_price : float
    tags : List[str]

#id here is a path parameter!!!
@app.get("/property/{id}")
async def test(id:int):
    try:
        return f"hi : {id}"
    except Exception as e:
        return "You are getting error ",e

@app.post("/add_product")
async def test1(product:Product):
    try:
        product.discounted_price = product.price - (product.price * product.discount) / 100

        return product
    except Exception as e:
        return f"You are getting error:: {e}"


if __name__ == "__main__":
    uvicorn.run(app=app,port=5000)

