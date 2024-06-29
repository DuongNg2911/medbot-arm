from pydantic import BaseModel

class ObjectDetectionViewModel(BaseModel):
    response_data: list

class ObjectDetectionImageViewModel(BaseModel):
    response_data: str