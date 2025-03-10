
"""
Django models for the Belvedere Glacier WebGIS application.

This module defines the main database tables.

"""

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `##managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.contrib.gis.db import models

class Measurements(models.Model):
    id = models.BigAutoField(primary_key=True)
    geom = models.GeometryField(blank=True, null=True)
    east = models.FloatField()
    north = models.FloatField()
    h = models.FloatField()
    point = models.ForeignKey('Points', models.DO_NOTHING, db_column='point')
    survey = models.ForeignKey('Surveys', models.DO_NOTHING, db_column='survey')
    point_photo = models.ForeignKey('PointPhoto', models.DO_NOTHING, db_column='point_photo', blank=True, null=True)
    meas_date = models.DateField(blank=True, null=True)
    ds_east = models.FloatField(blank=True, null=True)
    ds_north = models.FloatField(blank=True, null=True)
    ds_h = models.FloatField(blank=True, null=True)
    meas_strategy = models.CharField(max_length=25, blank=True, null=True)
    meas_time = models.DateTimeField(blank=True, null=True)
    notes = models.CharField(max_length=250, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    h_orto = models.FloatField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'measurements'


class Points(models.Model):
    id = models.BigAutoField(primary_key=True)
    label = models.CharField(unique=True, max_length=45)
    active = models.BooleanField()
    is_fixed = models.BooleanField(blank=True, null=True)
    ref_date = models.DateField(blank=True, null=True)
    notes = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'points'


class Surveys(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    year = models.BigIntegerField()
    notes = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'surveys'


class PointsMovementRaw(models.Model):
    id = models.IntegerField(primary_key=True) 
    geom = models.GeometryField()  
    label = models.CharField(max_length=255)  
    survey_year = models.IntegerField()  
    is_fixed = models.BooleanField()  
    survey_date_fin = models.DateField() 
    survey_date_prev = models.DateField(null=True, blank=True) 
    dt = models.FloatField()  
    east_fin = models.FloatField()  
    north_fin = models.FloatField() 
    h_fin = models.FloatField()  
    east_prev = models.FloatField(null=True, blank=True)  
    north_prev = models.FloatField(null=True, blank=True) 
    h_prev = models.FloatField(null=True, blank=True) 
    d_e = models.FloatField()  
    d_n = models.FloatField() 
    d_h = models.FloatField() 
    d = models.FloatField()  
    v_e = models.FloatField()  
    v_n = models.FloatField()  
    v_h = models.FloatField()  
    v = models.FloatField()  
    a_e = models.FloatField()  
    a_n = models.FloatField()  
    a_h = models.FloatField()  
    a = models.FloatField()

    class Meta:
        #managed = False
        db_table = 'points_movement_raw'


class Products2D(models.Model):
    id = models.BigAutoField(primary_key=True)
    fk_surveys = models.ForeignKey('Surveys', models.DO_NOTHING, db_column='fk_surveys', blank=True, null=True)
    data_type = models.CharField(max_length=254, blank=True, null=True)
    file_forma = models.CharField(max_length=254, blank=True, null=True)
    reference_field = models.CharField(db_column='reference_', max_length=254, blank=True, null=True)  
    epsg = models.BigIntegerField(blank=True, null=True)
    proj4 = models.CharField(max_length=254, blank=True, null=True)
    file_size_field = models.DecimalField(db_column='file_size_', max_digits=65535, decimal_places=65535, blank=True, null=True)  
    bounding_b = models.CharField(max_length=254, blank=True, null=True)
    license = models.CharField(max_length=254, blank=True, null=True)
    path = models.CharField(max_length=254, blank=True, null=True)
    pixel_size = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    n_bands = models.BigIntegerField(blank=True, null=True)

    class Meta:
        ##managed = False
        db_table = '2d_products'


class Products3D(models.Model):
    id = models.BigAutoField(primary_key=True)
    fk_surveys = models.ForeignKey('Surveys', models.DO_NOTHING, db_column='fk_surveys', blank=True, null=True)
    data_type = models.CharField(max_length=254, blank=True, null=True)
    file_forma = models.CharField(max_length=254, blank=True, null=True)
    reference_field = models.CharField(db_column='reference_', max_length=254, blank=True, null=True)  
    epsg = models.BigIntegerField(blank=True, null=True)
    proj4 = models.CharField(max_length=254, blank=True, null=True)
    file_size_field = models.DecimalField(db_column='file_size_', max_digits=65535, decimal_places=65535, blank=True, null=True)  
    bounding_b = models.CharField(max_length=254, blank=True, null=True)
    license = models.CharField(max_length=254, blank=True, null=True)
    path = models.CharField(max_length=254, blank=True, null=True)
    average_po = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    average_no = models.CharField(max_length=254, blank=True, null=True)
    n_points = models.BigIntegerField(blank=True, null=True)
    n_nodes = models.BigIntegerField(blank=True, null=True)
    n_scalar_f = models.BigIntegerField(blank=True, null=True)
    texture = models.IntegerField(blank=True, null=True)

    class Meta:
        ##managed = False
        db_table = '3d_products'


class Flights(models.Model):
    id = models.BigAutoField(primary_key=True)
    fk_surveys = models.ForeignKey('Surveys', models.DO_NOTHING, db_column='fk_surveys')
    average_he = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    n_images = models.BigIntegerField(blank=True, null=True)
    n_controlp = models.BigIntegerField(blank=True, null=True)
    n_checkpoi = models.BigIntegerField(blank=True, null=True)
    average_gs = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    camera_nam = models.CharField(max_length=254, blank=True, null=True)
    focal_leng = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    sensor_siz = models.CharField(max_length=254, blank=True, null=True)
    image_size = models.CharField(max_length=254, blank=True, null=True)
    pixel_size = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    global_acc = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    x_accuracy = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    y_accuracy = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    z_accuracy = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'flights'


class ImportMeasurementsTable(models.Model):
    id = models.BigAutoField(primary_key=True)
    point_label = models.CharField(max_length=45)
    survey_id = models.BigIntegerField()
    east = models.FloatField()
    north = models.FloatField()
    h = models.FloatField()
    point_photo = models.BigIntegerField(blank=True, null=True)
    meas_date = models.DateField(blank=True, null=True)
    meas_time = models.TimeField(blank=True, null=True)
    meas_strategy = models.CharField(max_length=25, blank=True, null=True)
    ds_east = models.FloatField(blank=True, null=True)
    ds_north = models.FloatField(blank=True, null=True)
    ds_h = models.FloatField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'import_measurements_table'


class Instruments(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=254, blank=True, null=True)
    type = models.CharField(max_length=254, blank=True, null=True)
    specificat = models.CharField(max_length=254, blank=True, null=True)
    brand = models.CharField(max_length=254, blank=True, null=True)
    year_of_m = models.BigIntegerField(blank=True, null=True)
    reseller = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'instruments'


class LayerStyles(models.Model):
    id = models.BigAutoField(primary_key=True)
    f_table_catalog = models.CharField(blank=True, null=True)
    f_table_schema = models.CharField(blank=True, null=True)
    f_table_name = models.CharField(blank=True, null=True)
    f_geometry_column = models.CharField(blank=True, null=True)
    stylename = models.TextField(blank=True, null=True)
    styleqml = models.TextField(blank=True, null=True)  
    stylesld = models.TextField(blank=True, null=True)  
    useasdefault = models.BooleanField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    owner = models.CharField(max_length=63, blank=True, null=True)
    ui = models.TextField(blank=True, null=True)  
    update_time = models.DateTimeField(blank=True, null=True)
    type = models.CharField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'layer_styles'


class PointsMeasurements(models.Model):
    id = models.BigAutoField(primary_key=True)
    point = models.ForeignKey('Points', models.DO_NOTHING, db_column='point')
    measurement = models.ForeignKey('Measurements', models.DO_NOTHING, db_column='measurement')

    class Meta:
        db_table = 'points_measurements'
        #managed = False

class PointPhoto(models.Model):
    id = models.BigAutoField(primary_key=True)
    path = models.CharField(max_length=254, blank=True, null=True)
    file_name = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'point_photo'


class QgisProjects(models.Model):
    name = models.TextField(primary_key=True)
    metadata = models.JSONField(blank=True, null=True)
    content = models.BinaryField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'qgis_projects'


class ScatterMeasurements(models.Model):
    id = models.BigAutoField(primary_key=True)
    point_id = models.BigIntegerField()
    survey = models.ForeignKey('Surveys', models.DO_NOTHING)
    geom = models.TextField(blank=True, null=True)  
    east = models.FloatField()
    north = models.FloatField()
    h = models.FloatField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'scatter_measurements'


class ScatterPoints(models.Model):
    id = models.BigAutoField(primary_key=True)
    label = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'scatter_points'


class SpatialRefSys(models.Model):
    srid = models.IntegerField(primary_key=True)
    auth_name = models.CharField(max_length=256, blank=True, null=True)
    auth_srid = models.IntegerField(blank=True, null=True)
    srtext = models.CharField(max_length=2048, blank=True, null=True)
    proj4text = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'spatial_ref_sys'


class SurveysHasInstruments(models.Model):
    id = models.BigAutoField(primary_key=True)
    fk_surveys = models.ForeignKey(Surveys, models.DO_NOTHING, db_column='fk_surveys', blank=True, null=True)
    fk_instrum = models.ForeignKey(Instruments, models.DO_NOTHING, db_column='fk_instrum', blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'surveys_has_instruments'

