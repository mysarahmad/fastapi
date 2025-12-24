from fastapi import FastAPI
import uvicorn
from database import Base
from database import engine

from routers.user import router


app = FastAPI()
app.include_router(router)

Base.metadata.create_all(engine)


if __name__ == "__main__":
    uvicorn.run(app=app,port=5000)
