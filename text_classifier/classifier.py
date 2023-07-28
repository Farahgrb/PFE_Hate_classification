# Import necessary libraries

import torch
from transformers import BertForSequenceClassification
from transformers import BertTokenizer
from pydantic import BaseModel
from utils.util import Singleton


# Define the model name to be used
Model_Used = "UBC-NLP/MARBERT"

# Define the HateSpeechDetector class
class HateSpeechDetector(metaclass=Singleton):
    def __init__(self):
        # Load the pre-trained model for sequence classification
        self.model = BertForSequenceClassification.from_pretrained(Model_Used, num_labels=3)

        # Load the model's state dictionary from a saved checkpoint
        model_state_dict = torch.load('/home/farah/Desktop/latest_version/Classification_fastapi/text_classifier/marbert_80.pth', map_location=torch.device('cpu'))
        self.model.load_state_dict(model_state_dict)

        # Load the tokenizer for the specific pre-trained model
        self.tokenizer = BertTokenizer.from_pretrained(Model_Used)

        # Define the class labels corresponding to each index
        self.class_labels = ["Normal", "Abusive", "Discrimination"]

    def detect_hate(self, text_body: str):
        # Tokenize the input text using the loaded tokenizer
        inputs = self.tokenizer(text_body, padding=True, truncation=True, return_tensors="pt")
        input_ids = inputs["input_ids"]
        attention_mask = inputs["attention_mask"]

        # Disable gradient calculation during inference
        with torch.no_grad():
            # Forward pass through the model
            outputs = self.model(input_ids, attention_mask=attention_mask)

        # Get the predicted labels by taking the argmax along the logits dimension
        predicted_labels = torch.argmax(outputs.logits, dim=1)

        # Get the predicted label and its probability score
        predicted_label = self.class_labels[predicted_labels.item()]
        probabilities = torch.softmax(outputs.logits, dim=1)
        predicted_probability = probabilities[0][predicted_labels.item()]
        print(text_body)
        # Create a dictionary containing the result (transcription and predicted label)
        result = {"Transcription": text_body, "label": predicted_label}

        return result


# Create an instance of the HateSpeechDetector class
hate_speech_detector = HateSpeechDetector()
