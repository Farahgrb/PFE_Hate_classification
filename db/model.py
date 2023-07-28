from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base=declarative_base()
class Detection(Base):
    __tablename__="detection"

    id=Column(String,primary_key=True)
    transcription=Column(String)
    firstlabel=Column(String)
    truelabel=Column(String)