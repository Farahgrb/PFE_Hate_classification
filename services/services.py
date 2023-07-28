from sqlalchemy.orm import Session
from db.model import Detection
from db.schemas import DetectionSchema
from typing import List
from text_classifier.classifier import hate_speech_detector
from db.crud import CrudOperations
import uuid
from pydantic import BaseModel
from typing import Optional


# Import the HateSpeechDetector class from your previous code
# Make sure the HateSpeechDetector class is available in the same directory or import it accordingly
# from hate_speech_detector import HateSpeechDetector
class id_text(BaseModel):
    id:Optional[str]=None

class HateSpeechService:
    def __init__(self):
        # Create an instance of the HateSpeechDetector class
        self.hate_speech_detector = hate_speech_detector
        self.crud= CrudOperations()


    def detect_hate_and_save(self, text: str):
   
        # Use the HateSpeechDetector to detect hate speech
        result = self.hate_speech_detector.detect_hate(text)

        # Create a new Detection record and save it to the database
        new_detection = {
            "id":str(uuid.uuid4()),
            "transcription":result["Transcription"],
            "firstlabel":result["label"],
            "truelabel":result["label"]
        }
        self.crud.create_detection(new_detection)


        return result

    def get_detections(self) -> List[Detection]:
        try:
            # Assuming 'crud' is an instance of the class that contains the 'get_detection' method
            return self.crud.get_detection()
        except Exception as e:
            print("Error get_detections:", e)
            return []

    def get_detection_by_id(self, detection_id: str) -> Detection:
        try:
            return self.crud.get_detection_by_id(detection_id)
        except:
            print("error while getting by id")

    def remove_detection(self, detection_id: str):
        try:
           self.crud.remove_detection(detection_id)
        except Exception as e:
            print("Error while removing:", e)





    def update_detection(self, detection_id: str,  truelabel: str) -> Detection:
        try:
            self.crud.update_detection(detection_id, truelabel)
        except Exception as e:
            print("error while updating:", e)
           
        return None
    
hate_services=HateSpeechService()

