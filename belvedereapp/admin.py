
"""
==============================================================================
Belvedere Glacier WebGIS - Django Admin Configuration
==============================================================================

This file configures the Django admin panel, allowing authorized users to 
manage database entries through a user-friendly interface. 

Key Features:
- Registers models to make them manageable via Django’s built-in admin interface.
- Enables quick data visualization and modification without requiring direct 
  database queries.
- Provides a structured and secure way to oversee the application's data.

Django's `admin.site.register(ModelName)` function is used to register each model, 
making them accessible in the Django admin dashboard.

==============================================================================
"""

from django.contrib import admin
from .models import (
    Products2D, Products3D, Flights, Instruments, Measurements, PointPhoto, 
    Points, ScatterMeasurements, ScatterPoints, Surveys, SurveysHasInstruments
)

admin.site.register([
    Products2D, Products3D, Flights, Instruments, Measurements, PointPhoto, 
    Points, ScatterMeasurements, ScatterPoints, Surveys, SurveysHasInstruments
])

