import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'services')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model')))
import numpy as np
import cv2
import io
import base64
import random

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from io import BytesIO
from PIL import Image
from contextlib import closing
from typing import Union
from tempfile import NamedTemporaryFile
from TextToSpeechServices import TextToSpeechServices
from ObjectDetectionServices import ObjectDetectionServices
from ObjectDetectionViewModel import ObjectDetectionViewModel

app = FastAPI()

@app.post("/SpeechToText/convertSpeechIntoText")
async def convertSpeechIntoText(data: UploadFile = File(...)):
    try:
        audio_bytes = await data.read()
        byte_stream = BytesIO(audio_bytes)
        with closing(NamedTemporaryFile(suffix=".webm", delete=False)) as temp_file:
            temp_file.write(byte_stream.getvalue())
            temp_file.flush()   
            transcribe = TextToSpeechServices("cpu", temp_file.name)
            text = transcribe.generate_text()
        return {"result": text}
    except Exception as error:
        return {"result": error} 

@app.post("/ObjectDetection/detectObject", response_model=list[ObjectDetectionViewModel])
async def detectObject(prompt: str, data: UploadFile = File(...)): 
    try:
        image_bytes = await data.read()
        
        # Convert bytes data to a NumPy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        
        # Decode the image using OpenCV
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        detector = ObjectDetectionServices("cpu") 
        result = detector.predict(image, prompt)

        return result
    except Exception as error:
        return {"result" : error}

@app.post("/ObjectDetection/detectObjectWithImageResponse")
async def detectObjectWithImageResponse(request: Request, prompt: str, data: UploadFile = File(...)): 
    try:
        image_bytes = await data.read()
        
        # Convert bytes data to a NumPy array
        nparr = np.frombuffer(image_bytes, np.uint8)
        
        # Decode the image using OpenCV
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        detector = ObjectDetectionServices("cpu") 
        result = detector.predict(image, prompt)
        for r in result:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            bounding_box = r["response_data"][:4]
            cv2.rectangle(image, (bounding_box[0], bounding_box[1]), (bounding_box[2], bounding_box[3]), color, 2)

        buffered = io.BytesIO()
        image = Image.fromarray(image)
        image.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()

        base64_string = base64.b64encode(img_bytes).decode('utf-8')
        encoded_image = "data:image/png;base64 " + base64_string

        return HTMLResponse(content=f"""
                    <html>
                    <body>
                        <div style="display: flex; flex-direction: column; padding: 10px">
                            <img
                                src="{encoded_image}"
                                alt="Image"
                                class="image"
                                height="50%"
                                width="50%"
                                style="margin: 0 auto"
                            />
                        </div>
                    </body>
                    </html>
                """)
    except Exception as error:
        return HTMLResponse(content=f"""
                    <html>
                    <body>
                        <div style="display: flex; flex-direction: column; padding: 10px">
                            Error
                        </div>
                    </body>
                    </html>
                """)