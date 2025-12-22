from fastapi import FastAPI
import uvicorn

app = FastAPI()

#id here is a path parameter!!!
@app.get("/property/{id}")
async def test(id:int):
    return f"hi : {id}"

if __name__ == "__main__":
    uvicorn.run(app=app,port=5000)

