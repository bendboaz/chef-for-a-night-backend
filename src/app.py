import uvicorn
from fastapi import FastAPI

from src import __version__
from src.common.constants import APP_NAME

app = FastAPI(title=APP_NAME, version=__version__)


@app.get('/')
def heartbeat():
    return "I'm alive!"


if __name__ == '__main__':
    uvicorn.run('app:app', host='localhost', reload=True)
