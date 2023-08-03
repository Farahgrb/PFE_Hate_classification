from sqlalchemy.orm import Session
from db.model import Detection
from db.schemas import DetectionSchema
from db.database import db_class, Database

class CrudOperations:
    def __init__(self):
        self.db = db_class
        self.session = self.db.get_session()
    def get_detection(self, skip: int = 0, limit: int = 500):
        return self.session.query(Detection).offset(skip).limit(limit).all()


    def get_detection_by_id(self, detection_id: str):

        return self.session.query(Detection).filter(Detection.id == detection_id).first()

    def create_detection(self, detection: DetectionSchema):
   
        _detection = Detection(id=detection['id'], transcription=detection["transcription"], firstlabel=detection["firstlabel"], truelabel=detection["truelabel"])
        
        self.session.add(_detection)
        self.session.commit()
        self.session.refresh(_detection)
        return _detection

    def remove_detection(self, detection_id: str):
 
        _detection = self.get_detection_by_id(detection_id)
        self.session.delete(_detection)
        self.session.commit()

    def update_detection(self, detection_id: str,  truelabel: str):
 
        _detection = self.get_detection_by_id(detection_id)

        _detection.truelabel = truelabel

        self.session.commit()
        self.session.refresh(_detection)
        return _detection
