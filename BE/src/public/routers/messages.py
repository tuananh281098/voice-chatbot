import base64
import io
import json
from typing import Literal, Union
from src.services.t2s_converter import T2SConverter
from fastapi import APIRouter
from fastapi.responses import StreamingResponse, PlainTextResponse
import requests

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
    converter = T2SConverter()
    audio = converter.convert(text=resp.json()[0]['text'])
    return {'audio': base64.b64encode(audio).decode("utf-8"), "text": resp.json()[0]['text']}
