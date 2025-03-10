
"""
==============================================================================
Belvedere Glacier WebGIS - URL Configuration
==============================================================================

This file defines the URL patterns for the `belvedereapp` Django application. 
It maps specific URLs to their corresponding view functions.

Key Features:
- Routes requests to appropriate views based on the URL.
- Handles the homepage, data upload, and login functionality.
- Uses Django's `path` function to define each route.

This file is essential for directing user navigation within the WebGIS platform.

==============================================================================
"""


from django.urls import path
from . import views
from .views import upload_data, login_view

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('login/', login_view, name="login"),  # Login page
    path('upload/', upload_data, name="upload_data"),  # Upload data page
]

