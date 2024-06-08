import easyocr
import cohere
from PIL import Image
import io
import json
import os

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Function to extract text from image using EasyOCR
def extract_text_with_easyocr(image_data):
    try:
        # Convert image data to Image object
        image = Image.open(io.BytesIO(image_data))
        # Read text from the image
        result = reader.readtext(image, detail=0)
        return result
    except Exception as e:
        print(f"Error occurred while extracting text: {e}")
        return []

# Function to use Cohere for text classification
def classify_text_with_cohere(api_key, extracted_text):
    try:
        co = cohere.Client(api_key)
        classifications = {}

        # Prepare a prompt for Cohere to classify the text
        prompt_template = '''Identify the following items in the extracted text:
        - First Name:
        - Middle Name:
        - Last Name:
        - Gender:
        - Street Address:
        - Postal Code:
        - ID Number:
        - Email:
        - City:
        - Country:
        - ID Type:
        - Birth Date:
        - Phone:
        - State:
        Text: {text}
        Category:'''

        # Join all extracted text into a single string
        text = '\n'.join(extracted_text)

        # Prepare the prompt
        prompt = prompt_template.format(text=text)
        
        # Generate response using Cohere
        response = co.generate(
            model='command-xlarge-nightly',  # Use an available model
            prompt=prompt,
            max_tokens=500,
            temperature=0.5
        )
        
        # Extract the classifications from the response
        response_text = response.generations[0].text.strip()
        
        # Split the response into individual classifications
        classification_lines = response_text.split('\n')
        
        # Iterate over each classification
        for line in classification_lines:
            key, value = line.strip().split(':')
            key = key.strip()
            value = value.strip()
            if value.lower() == 'not provided':
                classifications[key] = ''
            elif key.lower() == 'gender' and value.lower() in ['m', 'male']:
                classifications[key] = 'Male'
            elif key.lower() == 'gender' and value.lower() in ['f', 'female']:
                classifications[key] = 'Female'
            else:
                classifications[key] = value

        return classifications

    except Exception as e:
        print(f"An error occurred while using Cohere: {e}")
        return {}

def main(image_data):
    # Specify your Cohere API key here
    api_key = '18FuP1BbNmzBQhKPjxpbARCjhmdywwcMfsMyEEPg'

    # Extract text from image using EasyOCR
    extracted_text = extract_text_with_easyocr(image_data)

    # Classify the extracted text using Cohere
    classified_fields = classify_text_with_cohere(api_key, extracted_text)

    # Return the classified fields
    return classified_fields
