# Import necessary libraries

import torch
from transformers import BertForSequenceClassification
from transformers import BertTokenizer
from pydantic import BaseModel
from utils.util import Singleton
import re


# Define the model name to be used
Model_Used = "UBC-NLP/MARBERT"
def split_into_sentences(text):
    # Use a regular expression to split text into sentences
    sentences = re.split(r'\.|\?|!', text)
    # Filter out empty sentences
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    return sentences
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

    # def detect_hate(self, text_body: str):
    #     # Split text into sentences
    #     sentences = split_into_sentences(text_body)
        
    #     # Initialize variables to track the presence of "Discrimination" and "Abusive" sentences
    #     has_discrimination = False
    #     has_abusive = False
        
    #     for sentence in sentences:
    #         # Tokenize the sentence using the loaded tokenizer
    #         inputs = self.tokenizer(sentence, padding=True, truncation=True, return_tensors="pt")
    #         input_ids = inputs["input_ids"]
    #         attention_mask = inputs["attention_mask"]

    #         # Disable gradient calculation during inference
    #         with torch.no_grad():
    #             # Forward pass through the model
    #             outputs = self.model(input_ids, attention_mask=attention_mask)

    #         # Get the predicted labels by taking the argmax along the logits dimension
    #         predicted_labels = torch.argmax(outputs.logits, dim=1)

    #         # Get the predicted label and its probability score
    #         predicted_label = self.class_labels[predicted_labels.item()]
            
    #         # Check if the sentence is labeled as "Discrimination" or "Abusive"
    #         if predicted_label == "Discrimination":
    #             has_discrimination = True
    #         elif predicted_label == "Abusive":
    #             has_abusive = True

    #     # Predict the overall label based on the presence of "Discrimination" or "Abusive" sentences
    #     if has_discrimination:
    #         overall_label = "Discrimination"
    #     elif has_abusive:
    #         overall_label = "Abusive"
    #     else:
    #         overall_label = "Normal"

    #     # Create a dictionary containing the result (transcription and predicted label)
    #     result = {"Transcription": text_body, "label": overall_label}

    #     return result
    def detect_hate(self, text_body: str):
    #  a regular expression pattern to split Arabic text into sentences based on punctuation
       

     # Define a regular expression pattern to split text into sentences based on punctuation
        sentence_pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!|\،)\s'
        sentences = re.split(sentence_pattern, text_body)
        print(sentences)
    # Initialize a list to store the results (list of dictionaries)
        results = []

        for sentence in sentences:
            # Tokenize the sentence using the loaded tokenizer
            inputs = self.tokenizer(sentence, padding=True, truncation=True, return_tensors="pt")
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

            # Create a dictionary containing the result (transcription and predicted label)
            result = {"Transcription": sentence, "label": predicted_label}

            # Append the result dictionary to the results list
            results.append(result)

        return results

# Create an instance of the HateSpeechDetector class
hate_speech_detector = HateSpeechDetector()
