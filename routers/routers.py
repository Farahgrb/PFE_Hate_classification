from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from db.database import Database
from sqlalchemy.orm import Session
from db.schemas import DetectionSchema, Request, Response, RequestDetection,id_text
from services.services import hate_services
from pydantic import BaseModel
from typing import Optional


class TextInput(BaseModel):
    text: str

router = APIRouter()
class id_text(BaseModel):
    id:Optional[str]=None
class transcription(BaseModel):
    text:Optional[str]=None

@router.post("/classify_create")
async def create_classify(request: dict):
    print(request)
    result=hate_services.detect_hate_and_save(request["text"])
    print(result)
    return result
@router.get("/all")
async def get_detections():
    try:
        # Assuming 'hate_services' is an instance of the class that contains the 'get_detections' method
        _detections = hate_services.get_detections()
        print(_detections)
        return _detections
    except Exception as e:
        print("Error get_detections:", e)
        return []


@router.patch("/update")
async def update_detection(request:dict):
    _detection = hate_services.update_detection( detection_id=request["id"], truelabel=request["truelabel"])
    return Response(status="Ok", code="200", message="Success update data", result=_detection)


@router.delete("/delete")
async def delete_detection(request: id_text):
    
    hate_services.remove_detection(detection_id=request.id)
    return Response(status="Ok", code="200", message="Success delete data").dict(exclude_none=True)

@router.get("/{id}")
async def get_by_id(detection_id:id_text):
    _detection = hate_services.get_detection_by_id(detection_id=detection_id.id)
    return Response(code=200,status="ok", message="Success get data", result=_detection).dict(exclude_none=True)
