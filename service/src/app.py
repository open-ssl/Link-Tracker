import uvicorn
from fastapi import FastAPI
from utils.helpers import ConstConfig
from router import event_router

app = FastAPI(title=ConstConfig.PROJECT_TITLE)
app.include_router(event_router)

if __name__ == "__main__":
    uvicorn.run(app)
