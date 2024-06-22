from pydantic import BaseModel
from fastapi import File
from typing import Optional

class TextToSpeechRequests(BaseModel):
    data: bytes = File(...)
    # Model path
    path: Optional[str] = "models/ggml-small.bin"