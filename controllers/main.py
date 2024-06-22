import sys
# append dir 
sys.path.insert(0, 'medbot-arm/model')
sys.path.insert(1, 'medbot-arm/services')

from fastapi import FastAPI
from io import BytesIO
from contextlib import closing
from tempfile import NamedTemporaryFile
from services.TextToSpeechServices import TextToSpeechServices
from model.TextToSpeechRequests import TextToSpeechRequests

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
