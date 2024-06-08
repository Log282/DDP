# documents/urls.py
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    #path('', upload_docs, name='doc_upload'),
    #path('/media/docs/<str:doc_type>/<path:file_name>/', view_document, name='view_document'),
    #path('upload-docs/', upload_docs, name='upload_docs'),
    path('home/', home, name='home'),
    path('retrieve_recent_image/<str:document_type>/', retrieve_recent_image, name='retrieve_recent_image'),
    path('', login, name='login'),
    path('login_view/', login_view, name='login_view'),
    path('EDD/', edd, name='edd'),
    path('spDD', spdd, name='spdd'),
    path('entity/', entity, name='entity'),
    path('non-us-entity/', non_us_entity, name='non_us_entity'),
    path('us-entity/', us_entity, name='us_entity'),
    # path('home/new.html/', new, name='new'),
    path('us-consumer/', us_consumer, name='us_consumer'),
    path('non-us-consumer/', non_us_consumer, name='non_us_consumer'),
    path('new/', new_application, name='new_application'),
    path('saved-application/', save_application, name='save_application'),
    path('latest-image/', latest_uploaded_image, name='latest_uploaded_image'),
    path('get_data', get_data, name='get_data'),
    path('get_image', get_image, name='get_image'),



    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
