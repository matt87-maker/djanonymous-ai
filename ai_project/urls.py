from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ai/', include('ai.urls')),  # ✅ this routes /ai/generate/
]