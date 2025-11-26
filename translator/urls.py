from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_document, name='upload'),
    path('result/<int:doc_id>/', views.result_view, name='result'),
]
