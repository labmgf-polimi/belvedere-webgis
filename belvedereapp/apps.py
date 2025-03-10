
"""
==============================================================================
Belvedere Glacier WebGIS - Django App Configuration
==============================================================================

This file configures the Django application settings for `belvedereapp`. 

Key Features:
- Defines the application name (`belvedereapp`), which Django uses for app-specific configurations.
- Specifies the default type of primary key for database models (`BigAutoField`).
- Ensures the app is recognized when Django initializes.

This configuration is automatically created when a new Django app is initialized using:
    `python manage.py startapp belvedereapp`

==============================================================================
"""

from django.apps import AppConfig

class BelvedereappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'belvedereapp'
