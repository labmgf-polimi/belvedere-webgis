
"""
==============================================================================
Belvedere Glacier WebGIS - Views Module
==============================================================================

This module contains the core views (backend logic) for the Belvedere Glacier 
WebGIS application. It manages data processing, user authentication, and 
file uploads.

Main Functions:
- `home(request)`: Retrieves movement data, processes it by year and point, 
  computes averages when necessary, and converts coordinates for map visualization.
- `upload_data(request)`: Handles CSV file uploads, validates and stores data.
- `login_view(request)`: Manages user authentication, allowing access to 
  the upload functionality after successful login.

==============================================================================
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point

import json
import pandas as pd

from datetime import datetime
from pyproj import Proj, transform
from collections import defaultdict
from .models import PointsMovementRaw, Measurements, Points, Surveys

# Projection settings for coordinate transformation
utm_proj = Proj(init='epsg:32632')  # UTM zone 32N
wgs84_proj = Proj(init='epsg:4326')  # WGS84 (lat, lon)


def home(request):
    
    # Retrieve all measurement data from the database
    movement_data = PointsMovementRaw.objects.all()
    measurements_data = []
    
    # Group measurements by year and point label
    years = defaultdict(lambda: defaultdict(list))
    for measurement in movement_data:
        years[measurement.survey_year][measurement.label].append(measurement)

    # Process each year and its corresponding points
    for year, points in years.items():
        for point_label, point_measurements in points.items():
            if point_measurements:
                last_measurement = point_measurements[-1]
                
                # Compute average values if multiple measurements exist for the same year
                if len(point_measurements) > 1:
                    avg_values = {
                        'east': sum(m.east_fin for m in point_measurements) / len(point_measurements),
                        'north': sum(m.north_fin for m in point_measurements) / len(point_measurements),
                        'h': sum(m.h_fin for m in point_measurements) / len(point_measurements),
                        'd': point_measurements[0].d,
                        'v': round(sum(m.v for m in point_measurements) / len(point_measurements), 7),
                        'a': round(sum(m.a for m in point_measurements) / len(point_measurements), 7),
                    }
                    is_average = True
                else:
                    avg_values = {
                        'east': last_measurement.east_fin,
                        'north': last_measurement.north_fin,
                        'h': last_measurement.h_fin,
                        'd': last_measurement.d,
                        'v': round(last_measurement.v, 7),
                        'a': round(last_measurement.a, 7),
                    }
                    is_average = False

                # Convert UTM coordinates to latitude and longitude
                if isinstance(last_measurement.geom, Point):
                    lon, lat = transform(utm_proj, wgs84_proj, last_measurement.geom.x, last_measurement.geom.y)

                # Prepare data for the template
                measurements_data.append({
                    'id': last_measurement.id,
                    'label': last_measurement.label,
                    'label_title': last_measurement.label,
                    'is_fixed': last_measurement.is_fixed,
                    'survey_year': last_measurement.survey_year,
                    'lat': lat,
                    'lon': lon,
                    'alt': last_measurement.geom.z,
                    **avg_values,
                    'date': last_measurement.survey_date_fin.strftime("%Y-%m-%d"),
                    'is_average': is_average,
                })
    
    return render(request, 'home.html', {'measurements_data': json.dumps(measurements_data)})


@login_required
def upload_data(request):
    """
    Handles the upload and processing of a CSV file containing measurement data.
    - Validates the presence of required columns.
    - Extracts relevant data and inserts it into the database.
    - Dynamically retrieves all database fields to accommodate additional columns.

    Users must be authenticated to access this function.
    """

    if request.method == "POST":
        # Retrieve the uploaded CSV file
        csv_file = request.FILES.get("csv_file")
        if not csv_file:
            messages.error(request, "Please upload a CSV file.")
            return redirect("upload_data")

        try:
            # Read the CSV file into a Pandas DataFrame
            df = pd.read_csv(csv_file)
            
            # Define the required columns for the file to be processed
            required_columns = {"point", "meas_date", "east", "north", "h", "lat", "lon"}
            if not required_columns.issubset(df.columns):
                messages.error(request, "CSV file is missing required columns.")
                return redirect("upload_data")

            # Retrieve column names from the database models
            measurement_fields = {field.name for field in Measurements._meta.get_fields()}
            point_fields = {field.name for field in Points._meta.get_fields()}
            survey_fields = {field.name for field in Surveys._meta.get_fields()}

            for _, row in df.iterrows():
                try:
                    # Convert the date from string to a proper date format
                    meas_date = datetime.strptime(str(row["meas_date"]), "%Y-%m-%d").date()
                except ValueError:
                    messages.error(request, f"Invalid date format for {row['meas_date']}. Use YYYY-MM-DD.")
                    return redirect("upload_data")

                # Retrieve or create a point record
                point_data = {col: row[col] for col in point_fields if col in df.columns}
                # Ensure 'active' has a default value if not in CSV
                if "active" not in point_data:
                    point_data["active"] = True  # or False, depending on your logic
                point, _ = Points.objects.get_or_create(label=row["point"], defaults=point_data)

                # Retrieve or create a survey record
                survey_data = {col: row[col] for col in survey_fields if col in df.columns}
                survey_data["year"] = meas_date.year  # Ensure the correct year is set
                survey, _ = Surveys.objects.get_or_create(date=meas_date, defaults=survey_data)

                # Prepare measurement data with available fields from the CSV
                measurement_data = {col: row[col] for col in measurement_fields if col in df.columns}
                measurement_data["meas_date"] = meas_date
                measurement_data["survey"] = survey
                measurement_data["point"] = point

                # Insert the measurement data into the database
                Measurements.objects.create(**measurement_data)

            messages.success(request, "Upload completed successfully!")
        except Exception as e:
            messages.error(request, f"Error processing file: {str(e)}")
    
    # Render the upload form again, showing any messages if necessary
    return render(request, "upload_form.html")


def login_view(request):

    """
    Handles user authentication.
    - Checks if the provided username and password are valid.
    - If successful, logs the user in and redirects to the upload page.
    - If authentication fails, displays an error message.

    """

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("upload_data")  # Redirect to the upload page after login
        else:
            messages.error(request, "Invalid username or password. <br>Please try again.")

    return render(request, "login.html")
