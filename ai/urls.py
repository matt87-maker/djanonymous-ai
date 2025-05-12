from django.urls import path
from .views import generate_text, home

urlpatterns = [
    path("", home),                 # Homepage with prompt form
    path("generate/", generate_text),  # API endpoint
]