import easyocr
import cohere

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Function to extract text from image using EasyOCR
def extract_text_with_easyocr(image_path):
    try:
        # Read text from the image
        result = reader.readtext(image_path, detail=0)
        return result
    except Exception as e:
        print(f"Error occurred while extracting text: {e}")
        return []

# Function to use Cohere for text classification
def classify_text_with_cohere(api_key, extracted_text):
    co = cohere.Client(api_key)
    classifications = {}

    # Prepare a prompt for Cohere to classify the text
    prompt_template = '''Identify the following items in the extracted text:
- First Name :
- Middle Name:
- Last Name:
- Gender :
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
- Date of Issue:
- Date of Expiry:
Text: {text}
Category:'''

    # Join all extracted text into a single string
    text = '\n'.join(extracted_text)

    try:
        # Prepare the prompt
        prompt = prompt_template.format(text=text)
        
        # Generate response using Cohere
        response = co.generate(
            model='command-r-plus',  # Use an available model
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

    except Exception as e:
        print(f"An error occurred: {e}")

    return classifications

def main(image_path, api_key):
    # Extract text from image using EasyOCR
    extracted_text = extract_text_with_easyocr(image_path)

    # Classify the extracted text using Cohere
    classified_fields = classify_text_with_cohere(api_key, extracted_text)

    # Print the classified fields as key-value pairs
    print("Output:")
    for key, value in classified_fields.items():
        print(f"{key}: {value}")

# Replace 'your_cohere_api_key' with your actual Cohere API key
api_key = 'MSlQOlC8HTBfCAMUvS7VNdOsvnTm194IJUWxm8pv'

# Replace 'path_to_your_image.jpg' with the actual image path
image_path = r"photo id/Oklahoma's.jpg"

# Call the main function
main(image_path, api_key)




#     prompt_template = '''Identify the following items in the extracted text:
# - First Name:
# - Middle Name:
# - Last Name:
# - Gender:
# - Street Address:
# - Postal Code:
# - ID Number:
# - Email:
# - City:
# - Country:
# - ID Type:
# - Birth Date(dd/mm/yyyy):
# - Phone:
# - State:
# Text: {text}
# Category:'''