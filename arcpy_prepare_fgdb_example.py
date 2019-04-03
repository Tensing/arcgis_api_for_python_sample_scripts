## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## Script: arcpy_prepare_fgdb_example.py
## Goal: create a File Geodatabase with 3 Feature Classes with domains and with editor tracking and attachments enabled
## Author: Egge-Jan Polle - Tensing GIS Consultancy
## Date: April 3, 2019
## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# This script should be run within a specific ArcGIS/Python environment using the batch file below
# (This batch file comes with the installation of ArcGIS Pro)
# "C:\Program Files\ArcGIS\Pro\bin\Python\scripts\propy.bat" arcpy_prepare_fgdb_example.py
#
# Import system modules
import os, zipfile, arcpy, csv
from arcpy import env
import domain_definitions

# Overwrite pre-existing files
env.overwriteOutput = True

# Define the coordinate system to be used for the feature classes - in this example we do use the Dutch system RD_New (EPSG: 28992)
coord_sys = "PROJCS['RD_New',GEOGCS['GCS_Amersfoort',DATUM['D_Amersfoort',SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Double_Stereographic'],PARAMETER['False_Easting',155000.0],PARAMETER['False_Northing',463000.0],PARAMETER['Central_Meridian',5.38763888888889],PARAMETER['Scale_Factor',0.9999079],PARAMETER['Latitude_Of_Origin',52.15616055555555],UNIT['Meter',1.0]];-30515500 -30279500 10000;-100000 10000;-100000 10000;0,001;0,001;0,001;IsHighPrecision"

# Database to be created
fgdb = 'MY_NEW_FGDB.gdb'

# Read the fields and their properties from a separate CSV file
feature_class_fields = 'feature_class_fields.csv'

editor_tracking_fields = [['CREATED_USER','Created by'],['CREATED_DATE','Created on'],['LAST_EDITED_USER','Last modified by'],['LAST_EDITED_DATE','Last modified on']]

feature_classes=[["MY_POINTS","POINT"],["MY_LINES","POLYLINE"],["MY_POLYGONS","POLYGON"]]

print('===================')
print('The script that is running: ' + __file__)
print ("Start: "+datetime.datetime.today().strftime('%c'))
print('===================')

my_gdb = arcpy.CreateFileGDB_management(os.path.dirname(os.path.realpath(__file__)),fgdb)

print (datetime.datetime.today().strftime('%c')+": File Geodatabase has been created")


# All domains will be created from a list in an external file: domain_definitions.py
domain_definitions.create_domains(my_gdb)

print (datetime.datetime.today().strftime('%c')+": Domains have been created")

for feature_class in feature_classes:
    feature_class_created = arcpy.CreateFeatureclass_management(out_path=my_gdb, out_name=feature_class[0], geometry_type=feature_class[1], template="", has_m="DISABLED", has_z="DISABLED", spatial_reference=coord_sys, config_keyword="", spatial_grid_1="0", spatial_grid_2="0", spatial_grid_3="0")

    with open(feature_class_fields) as infile:
        new_fields  = csv.DictReader(infile, delimiter = ';')

        for new_field in new_fields:
            arcpy.AddField_management(in_table=feature_class_created,field_name=new_field['v_field_name'],field_type=new_field['v_field_type'],field_precision="",field_scale="",field_length=new_field['v_field_length'],field_alias=new_field['v_field_alias'],field_is_nullable="NULLABLE",field_is_required="NON_REQUIRED",field_domain=new_field['v_field_domain'])

    # Create fields for Editor Tracking (this is not obligatory - the fields can also be created automatically by the EnableEditorTracking_management function.
    # Here we create these fields to be able to manage the field_aliases
    arcpy.AddField_management(in_table=feature_class_created,field_name=editor_tracking_fields[0][0],field_type="TEXT",field_precision="",field_scale="",
                                field_length="50",field_alias=editor_tracking_fields[0][1],field_is_nullable="NULLABLE",field_is_required="NON_REQUIRED",field_domain="")
    arcpy.AddField_management(in_table=feature_class_created,field_name=editor_tracking_fields[1][0],field_type="DATE",field_precision="",field_scale="",
                                field_length="",field_alias=editor_tracking_fields[1][1],field_is_nullable="NULLABLE",field_is_required="NON_REQUIRED",field_domain="")
    arcpy.AddField_management(in_table=feature_class_created,field_name=editor_tracking_fields[2][0],field_type="TEXT",field_precision="",field_scale="",
                                field_length="50",field_alias=editor_tracking_fields[2][1],field_is_nullable="NULLABLE",field_is_required="NON_REQUIRED",field_domain="")
    arcpy.AddField_management(in_table=feature_class_created,field_name=editor_tracking_fields[3][0],field_type="DATE",field_precision="",field_scale="",
                                field_length="",field_alias=editor_tracking_fields[3][1],field_is_nullable="NULLABLE",field_is_required="NON_REQUIRED",field_domain="")
    #Enable Editor Tracking
    arcpy.EnableEditorTracking_management(in_dataset=feature_class_created,creator_field=editor_tracking_fields[0][0],creation_date_field=editor_tracking_fields[1][0],
                                last_editor_field=editor_tracking_fields[2][0],last_edit_date_field=editor_tracking_fields[3][0],add_fields="",record_dates_in="UTC")
    # Enable attachments
    arcpy.EnableAttachments_management(in_dataset=feature_class_created)
    # # Optionally: Add Global IDs
    # arcpy.AddGlobalIDs_management(feature_class_created)

print (datetime.datetime.today().strftime('%c')+": Feature classes have been added, with global ids, editor tracking and attachments enabled")
print('===================')
print ("Ready: "+datetime.datetime.today().strftime('%c'))
print('===================')

print('Do you want to zip the File Geodatabase {} immediately?'.format(fgdb))
answer = input('y/yes or n/no >>').lower()
if answer in ['yes', 'y']:
    zip_file_name = '{}.zip'.format(fgdb)

    # Opening the 'Zip' in writing mode
    with zipfile.ZipFile(zip_file_name, 'w') as file:
        # write mode overrides all the existing files in the 'Zip.'
        file.write(fgdb)
        print (datetime.datetime.today().strftime('%c')+": File Geodatabase has been zipped")

print('===================')
print ("Ready: "+datetime.datetime.today().strftime('%c'))
print('===================')
