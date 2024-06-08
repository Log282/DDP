from django.db import models
from django.utils.timezone import now

class KYC_Primary(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('drivers_license', 'Driver\'s License'),
        ('passport', 'Passport'),
        ('govt_photo_id', 'Government Photo ID'),
        ('us_armed_forces_id', 'U.S Armed Forces ID'),
        ('us_alien_registration_card', 'U.S Alien Registration Card'),
        ('permanent_resident_card', 'Permanent Resident Card'),
        # Add other choices as needed
    ]

    document_type = models.CharField(max_length=100, choices=DOCUMENT_TYPE_CHOICES, default='drivers_license')  # Provide a default

    document = models.ImageField(upload_to='docs/', null=True, blank=True)



# models.py

from django.db import models

class PrimaryDocument(models.Model):
    document_type = models.CharField(max_length=100)
    file = models.FileField(upload_to='primary_documents/')

class SecondaryDocument(models.Model):
    document_type = models.CharField(max_length=100)
    file = models.FileField(upload_to='secondary_documents/')

class NonDocumentaryVerification(models.Model):
    document_type = models.CharField(max_length=100)
    file = models.FileField(upload_to='non_documentary_verification/')



class NewApplications(models.Model):
    document_type = models.CharField(max_length=100)
    file = models.FileField(upload_to='new_application_documents/')  # Adjusted path
    upload_date = models.DateTimeField(default=now)  # Added upload date field

    def __str__(self):
        return f"{self.document_type} - {self.upload_date}"

class ApplicationData(models.Model):
    unique_id = models.CharField(max_length=100, unique=True)
    mname = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    add = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    idno = models.CharField(max_length=100, blank=True, null=True)
    # acc_type = models.CharField(max_length=100, blank=True, null=True)
    lname = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    fname = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    phn = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    id_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.unique_id

