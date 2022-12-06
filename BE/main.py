import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(current)
sys.path.append(parent)

import src.public.routers.messages as message_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(message_router.router)

@app.get('/', response_model=str)
def ping():
    build_date = os.getenv("BUILD_DATE")
    return f'Alive, last built: {build_date}'
