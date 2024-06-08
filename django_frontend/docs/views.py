from django.shortcuts import render, redirect
from .models import KYC_Primary
from .forms import DocumentUploadForm
from django.http import JsonResponse, HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from .cohere1 import main  # Import main function from cohere.py
import os
from django.conf import settings
from .models import PrimaryDocument, SecondaryDocument, NonDocumentaryVerification
from .models import ApplicationData

from django.core.files.storage import FileSystemStorage
import easyocr
import cohere
from cohere.errors import BadRequestError,TooManyRequestsError,InternalServerError,ServiceUnavailableError
import json

import json
import os
import random
import string
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# import pyautogui as pag

from django.core.exceptions import ValidationError
from .models import *


def new_application(request):
  classified_fields = {}

  if request.method == 'POST' and request.FILES.get('fileInput'):
    file = request.FILES['fileInput']

    # Generate a random alphanumeric 8-digit filename with extension
    filename, extension = os.path.splitext(file.name)
    new_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=8)) + extension

    # Save the uploaded file with the original name (preserves path)
    try:
      new_doc = NewApplications(document_type="ID", file=file)
      new_doc.save()
    except ValidationError as e:
      print(f"Validation error: {e}")
      return render(request, 'new.html', {'error': "Invalid file upload"})

    # Store the original filename for reference (optional)
    original_filename = file.name

    # Access image path from the saved model instance (unchanged)
    image_path = new_doc.file.path

    # Process the uploaded file using the image_path (unchanged)
    reader = easyocr.Reader(['en'])
    extracted_text = reader.readtext(image_path, detail=0)
    print("Extracted text:", extracted_text)

    co = cohere.Client('MSlQOlC8HTBfCAMUvS7VNdOsvnTm194IJUWxm8pv')  # Replace with your API key

    text = '\n'.join(extracted_text)
    print("Joined text:", text)

    prompt_template = '''Identify the following items in the extracted text:
      FirstName (if more than one name seperated by space, include all as first name):
      MiddleName:
      LastName:
      Gender (check if text includes SEX:M i.e Male and SEX:F i.e Female):
      StreetAddress:
      PostalCode:
      IDNumber:
      Email:
      City:
      Country:
      IDType:
      BirthDate:
      Phone:
      State:
      DateOfIssue:
      DateOfExpiry:
      Text: {text}
      Category:

     '''

    try:
      prompt = prompt_template.format(text=text)
      print("Prompt:", prompt)

      response = co.generate(
          model='command-xlarge-nightly',
          prompt=prompt,
          max_tokens=500,
          temperature=0.3
      )

      print("Response:", response)

      response_text = response.generations[0].text.strip()
      print("Response text:", response_text)

      classification_lines = response_text.split('\n')

      for line in classification_lines:
        if ':' in line:
          key, value = line.strip().split(':', 1)
          key = key.strip()
          value = value.strip()
          if value.lower() == 'not provided':
            classified_fields[key] = ''
          elif key.lower() == 'gender' and value.lower() in ['m', 'male']:
            classified_fields[key] = 'Male'
          elif key.lower() == 'gender' and value.lower() in ['f', 'female']:
            classified_fields[key] = 'Female'
          else:
            classified_fields[key] = value

    except Exception as e:
      print(f"An error occurred: {e}")
      return render(request, 'new.html', {'error': "Processing error"})

  return render(request, 'new.html', {'classified_fields': classified_fields})

    # # Clean up the temporary file if a new image is uploaded
    # if temp_file_path:
    #     try:
    #         os.remove(temp_file_path)
    #     except OSError as e:
    #         print(f"Error: {e.strerror}")

# def generate_unique_id(length=5):                                                    #divyal
#     return ''.join(random.choices(string.ascii_letters + string.digits, k=length))   #divyal

#new-ranjith
def generate_unique_id(id_type):
    id_type = id_type.lower()  # Convert to lowercase for uniformity
    prefix = 'ID'
    if id_type in  ['driver licence','driving licence','driver license','driving license',"driver's license","driver's licence"]:
        prefix = 'DL'
    elif id_type in ['passport', 'official travel document']:
        prefix = 'PP'
    
    random_numbers = ''.join(random.choices(string.digits, k=4))
    return f'{prefix}{random_numbers}'

def latest_uploaded_image(request):
    latest_application = NewApplications.objects.latest('upload_date')
    image_path = latest_application.file.url  # Assuming file is a FileField
    return render(request, 'latest_image.html', {'image_path': image_path})

@csrf_exempt
def save_application(request):
    if request.method == 'POST':
        data = {
            'FirstName': request.POST.get('FirstName', ''),
            'Gender': request.POST.get('Gender', ''),
            'StreetAddress': request.POST.get('StreetAddress', ''),
            'PostalCode': request.POST.get('PostalCode', ''),
            'IDNumber': request.POST.get('IDNumber', ''),
            'DateOfIssue': request.POST.get('DateOfIssue', ''),
            'MiddleName': request.POST.get('MiddleName', ''),
            'Email': request.POST.get('Email', ''),
            'City': request.POST.get('City', ''),
            'Country': request.POST.get('Country', ''),
            'IDType': request.POST.get('IDType', ''),
            'DateOfExpiry': request.POST.get('DateOfExpiry', ''),
            'LastName': request.POST.get('LastName', ''),
            'BirthDate': request.POST.get('BirthDate', ''),
            'Phone': request.POST.get('Phone', ''),
            'State': request.POST.get('State', '')
        }

        latest_application = NewApplications.objects.latest('upload_date')

        # Get the file path of the latest uploaded file 
        latest_file_path = latest_application.file.path

        # Include the file path in the JSON data
        data['DocumentPath'] = latest_file_path

        unique_id = generate_unique_id(data['IDType'])
        file_path = os.path.join('C:\\Users\\user\\Desktop\\DDP\\django_frontend\\data', f'{unique_id}.json')

        try:
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file)
            print("Data saved to JSON:", data)
            return JsonResponse({'message': 'Data saved successfully.', 'unique_id': unique_id}, status=200)
        except Exception as e:
            print("Error saving data:", e)
            return JsonResponse({'message': 'Failed to save data.', 'error': str(e)}, status=500)

    return JsonResponse({'message': 'Invalid request method.'}, status=400)

# def fetch_application_data(request, unique_id):                                       #LOGESH-NEW
#     try:
#         application_data = ApplicationData.objects.get(unique_id=unique_id)
#         data = {
#             'status': 'success',
#             'mname': application_data.middle_name,
#             'gender': application_data.gender,
#             'street_address': application_data.street_address,
#             'postal_code': application_data.postal_code,
#             'id_number': application_data.id_number,
#             # 'account_type': application_data.account_type,
#             'lname': application_data.last_name,
#             'email': application_data.email,
#             'city': application_data.city,
#             'country': application_data.country,
#             'fname': application_data.first_name,
#             'birth_date': application_data.birth_date,
#             'phone': application_data.phone_number,
#             'state': application_data.state,
#             'id_type': application_data.id_type,
#         }
#     except ApplicationData.DoesNotExist:
#         data = {'status': 'error', 'message': 'Application data not found'}

#     return JsonResponse(data)

def get_data(request):
    app_id = request.GET.get('appId')
    if not app_id:
        return JsonResponse({'error': 'Application ID is required'}, status=400)
    
    data_folder = 'C:\\Users\\user\\Desktop\\DDP\\django_frontend\\data'
    file_path = os.path.join(data_folder, f'{app_id}.json')
    
    if not os.path.isfile(file_path):
        return JsonResponse({'error': 'Application ID does not exist'}, status=404)

    with open(file_path, 'r') as file:
        data = json.load(file)
    
    return JsonResponse(data)


def get_image(request):
    app_id = request.GET.get('appId')
    if not app_id:
        raise Http404("Application ID is required")

    data_folder = 'C:\\Users\\user\\Desktop\\DDP\\django_frontend\\data'
    file_path = os.path.join(data_folder, f'{app_id}.json')
    
    if not os.path.isfile(file_path):
        raise Http404("Application ID does not exist")
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    document_path = data.get('DocumentPath')
    if not document_path or not os.path.isfile(document_path):
        raise Http404("Document not found")
    
    with open(document_path, 'rb') as image:
        return HttpResponse(image.read(), content_type="image/jpeg")




@csrf_exempt
def home(request):
    if request.method == 'POST':
        primary_document_type = request.POST.get('primary_document_type')
        primary_document_file = request.FILES.get('fileInput1')
        PrimaryDocument.objects.create(document_type=primary_document_type, file=primary_document_file)

        secondary_document_type = request.POST.get('secondary_document_type')
        secondary_document_file = request.FILES.get('fileInput2')
        SecondaryDocument.objects.create(document_type=secondary_document_type, file=secondary_document_file)

        non_documentary_type = request.POST.get('non_documentary_type')
        non_documentary_file = request.FILES.get('fileInput3')
        NonDocumentaryVerification.objects.create(document_type=non_documentary_type, file=non_documentary_file)

        print("Documents uploaded successfully")  

        #return HttpResponse(json.dumps({'success': True}), content_type="application/json")
    return render(request, 'home-index.html')


def retrieve_recent_image(request, document_type):
    document_folder = ''
    if document_type == 'primary':
        document_folder = 'primary_documents/'
    elif document_type == 'secondary':
        document_folder = 'secondary_documents/'
    elif document_type == 'non_documentary':
        document_folder = 'non_documentary_verification/'

    document_path = os.path.join(settings.MEDIA_ROOT, document_folder)
    files = os.listdir(document_path)
    
    if files:
        # Sort files based on modification time
        files.sort(key=lambda x: os.path.getmtime(os.path.join(document_path, x)), reverse=True)
        latest_file = files[0]  # Get the most recently modified file

        # Get the path to the latest file
        image_path = os.path.join(document_folder, latest_file)

        # Open and read the image data
        with open(os.path.join(settings.MEDIA_ROOT, image_path), 'rb') as f:
            image_data = f.read()
        
        # Return the image data in the HTTP response
        return HttpResponse(image_data, content_type="image/png")  # Assuming the image type is PNG
    else:
        return HttpResponse("No image found", status=404)


def login(request):
    return render(request, 'login.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authentication successful for any username and password
        request.session['logged_in'] = True  # Set a session variable to indicate login status
        return redirect('home')  # Redirect to the home page

    else:
        return render(request, 'login.html')

def edd(request):
    return render(request, 'EDD.html')

def entity(request):
    return render(request, 'entity.html')

def non_us_consumer(request):
    return render(request, 'non-us-consumer.html')

def non_us_entity(request):
    return render(request, 'non-us-entity.html')

def spdd(request):
    return render(request, 'spDD.html')

def us_consumer(request):
    return render(request, 'us-consumer.html')

def us_entity(request):
    return render(request, 'us-entity.html')

