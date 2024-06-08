from django import forms
from .models import KYC_Primary

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = KYC_Primary
        fields = ['document_type', 'document']

    def save(self, commit=True):
        document_type = self.cleaned_data.get('document_type')
        document = self.cleaned_data.get('document')
        existing_instance = KYC_Primary.objects.filter(document=document.name, document_type=document_type).first()
        
        if existing_instance:
            existing_instance.document = document
            #existing_instance.save()
            return existing_instance
        else:
            instance = super().save(commit=False)
            directory = f'docs/{document_type}/'
            instance.document.storage.save(directory + document.name, document)
            if commit:
                instance.save()
            return instance
