from typing import List,Optional, Generic,TypeVar
from pydantic import BaseModel,Field
from pydantic.generics import GenericModel

T = TypeVar("T")

class DetectionSchema(BaseModel):
    id:Optional[str]=None
    transcription:Optional[str]=None
    firstlabel:Optional[str]=None
    truelabel:Optional[str]=None
    class Config:
        orm_mode = True

class id_text(BaseModel):
    id:Optional[str]=None
    
class Request(GenericModel, Generic[T]):
    parameter: Optional[T] = Field(...)


class RequestDetection(BaseModel):
    parameter: DetectionSchema = Field(...)


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]