## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## Script: arcpy_prepare_fgdb_example.py
## Goal: create a File Geodatabase with 3 Feature Classes with domains and with editor tracking and attachments enabled
## Author: Egge-Jan Polle - Tensing GIS Consultancy
## Date: August 9, 2018
## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# This script should be run within a specific ArcGIS/Python environment using the batch file below
# (This batch file comes with the installation of ArcGIS Pro)
# "C:\Program Files\ArcGIS\Pro\bin\Python\scripts\propy.bat" arcpy_prepare_fgdb_example.py
#
# Import system modules
import os
import arcpy, csv
from arcpy import env
import domain_definitions

# Overwrite pre-existing files
env.overwriteOutput = True

rd_new = "PROJCS['RD_New',GEOGCS['GCS_Amersfoort',DATUM['D_Amersfoort',SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Double_Stereographic'],PARAMETER['False_Easting',155000.0],PARAMETER['False_Northing',463000.0],PARAMETER['Central_Meridian',5.38763888888889],PARAMETER['Scale_Factor',0.9999079],PARAMETER['Latitude_Of_Origin',52.15616055555555],UNIT['Meter',1.0]];-30515500 -30279500 10000;-100000 10000;-100000 10000;0,001;0,001;0,001;IsHighPrecision"

feature_class_fields = 'feature_class_fields.csv'

editor_tracking_fields = ['CREATED_USER','CREATED_DATE','LAST_EDITED_USER','LAST_EDITED_DATE']

feature_classes=[["MY_POINTS","POINT"],["MY_LINES","POLYLINE"],["MY_POLYGONS","POLYGON"]]

print('===================')
print('The script that is running: ' + __file__)
print ("Start: "+datetime.datetime.today().strftime('%c'))
print('===================')

my_gdb = arcpy.CreateFileGDB_management(os.path.dirname(os.path.realpath(__file__)),"MY_NEW_FGDB.gdb")

print (datetime.datetime.today().strftime('%c')+": File Geodatabase has been created")


# All domains will be created from a list in an external file: domain_definitions.py
domain_definitions.create_domains(my_gdb)

print (datetime.datetime.today().strftime('%c')+": Domains have been created")

for feature_class in feature_classes:
    feature_class_created = arcpy.CreateFeatureclass_management(out_path=my_gdb, out_name=feature_class[0], geometry_type=feature_class[1], template="", has_m="DISABLED", has_z="DISABLED", spatial_reference=rd_new, config_keyword="", spatial_grid_1="0", spatial_grid_2="0", spatial_grid_3="0")

    with open(feature_class_fields) as infile:
        new_fields  = csv.DictReader(infile, delimiter = ';')

        for new_field in new_fields:
            arcpy.AddField_management(in_table=feature_class_created,field_name=new_field['v_field_name'],field_type=new_field['v_field_type'],field_precision="",field_scale="",field_length=new_field['v_field_length'],field_alias=new_field['v_field_alias'],field_is_nullable="NULLABLE",field_is_required="NON_REQUIRED",field_domain=new_field['v_field_domain'])

    # Create fields for Editor Tracking (this is not obligatory - the fields can also be created automatically by the EnableEditorTracking_management function.
    # Here we create these fields to be able to manage the field_aliases
    arcpy.AddField_management(in_table=feature_class_created,field_name=editor_tracking_fields[0],field_type="TEXT",field_precision="",field_scale="",field_length="50",field_alias="Created by",field_is_nullable="NULLABLE",field_is_required="NON_REQUIRED",field_domain="")
    arcpy.AddField_management(in_table=feature_class_created,field_name=editor_tracking_fields[1],field_type="DATE",field_precision="",field_scale="",field_length="",field_alias="Created on",field_is_nullable="NULLABLE",field_is_required="NON_REQUIRED",field_domain="")
    arcpy.AddField_management(in_table=feature_class_created,field_name=editor_tracking_fields[2],field_type="TEXT",field_precision="",field_scale="",field_length="50",field_alias="Last modified by",field_is_nullable="NULLABLE",field_is_required="NON_REQUIRED",field_domain="")
    arcpy.AddField_management(in_table=feature_class_created,field_name=editor_tracking_fields[3],field_type="DATE",field_precision="",field_scale="",field_length="",field_alias="Last modified on",field_is_nullable="NULLABLE",field_is_required="NON_REQUIRED",field_domain="")
    #Enable Editor Tracking
    arcpy.EnableEditorTracking_management(in_dataset=feature_class_created,creator_field=editor_tracking_fields[0],creation_date_field=editor_tracking_fields[1],last_editor_field=editor_tracking_fields[2],last_edit_date_field=editor_tracking_fields[3],add_fields="",record_dates_in="UTC")
    # Enable attachments
    arcpy.EnableAttachments_management(in_dataset=feature_class_created)

print (datetime.datetime.today().strftime('%c')+": Feature classes have been added, with editor tracking and attachments enabled")
print('===================')
print ("Ready: "+datetime.datetime.today().strftime('%c'))
print('===================')