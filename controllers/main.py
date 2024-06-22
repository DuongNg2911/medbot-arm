import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'services')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model')))

from fastapi import FastAPI
from io import BytesIO
from contextlib import closing
from tempfile import NamedTemporaryFile
from TextToSpeechServices import TextToSpeechServices
from TextToSpeechRequests import TextToSpeechRequests

app = FastAPI()

@app.get("/SpeechToText/convertSpeechIntoText")
async def convertSpeechIntoText(request_data: TextToSpeechRequests):
    try:
        byte_stream = BytesIO(request_data.data)
        with closing(NamedTemporaryFile(suffix=".webm", delete=False)) as temp_file:
            temp_file.write(byte_stream.getvalue())
            temp_file.flush()   
            text = await TextToSpeechServices("cpu", request_data.model_path, temp_file.name)

        return {"result": text}
    except Exception as error:
        return {"result": error} 

# @app.get("/ObjectDetection/")
