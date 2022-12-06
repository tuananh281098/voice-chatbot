import json
from typing import Literal, Union
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse, PlainTextResponse
import requests

from src.service_register import get_t2s_converter
from src.services.t2s_converter import T2SConverter

router = APIRouter(prefix='/messages', tags=['messages'])

rasa_url = "http://localhost:5005"

@router.put(":input")
def input_text(text: str, format: Literal["text", "audio"] = "text"):
    resp = requests.post(
        url=f"{rasa_url}/webhooks/rest/webhook",
        headers={"Content-Type": "application/json"},
        data=json.dumps({
            "sender": "test_user",
            "message": text,
        }),
        timeout=30,
    )
    print(resp)
    return resp.json()
    # audio = t2s_converter.convert(text=text)
    # return StreamingResponse(content=audio, media_type="audio/mpeg")
