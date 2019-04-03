## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## Script: agol_publish_fc_from_fgdb_to_featureserver_layer.py
## Goal: to publish a Feature Class from a File Geodatabase to a FeatureServer Layer
## Author: Egge-Jan Polle - Tensing GIS Consultancy
## Date: April 3, 2019
## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# This script should be run within a specific ArcGIS/Python environment using the batch file below
# (This batch file comes with the installation of ArcGIS Pro)
# "C:\Program Files\ArcGIS\Pro\bin\Python\scripts\propy.bat" agol_publish_fc_from_fgdb_to_featureserver_layer.py
#
import os, datetime
from arcgis.gis import GIS
from provide_credentials import provide_credentials

# Variables to complete before publishing the service =====================================================================================
# data - The path to the zip file containing the input File Geodatabase
# E.g.'C:/Data/MY_NEW_FGDB.gdb.zip'
data = ''
# service_name - The name of the FeatureServer
# E.g. 'MY_VERY_FIRST_FEATURE_SERVER'
service_name = 'MY_VERY_FIRST_FEATURE_SERVER_TEST'
# service_description - Description of the item. In the Dutch interface: "Beschrijving"
# E.g. 'Here you can put a description of the Feature Layer'
service_description = 'Here you can put a description of the Feature Layer'
# service_snippet - Provide a short summary (limit to max 250 characters) of the what the item is.
# E.g. 'Here you can put a short snippet describing the Feature Layer'
service_snippet = 'Here you can put a short snippet describing the Feature Layer'
# service_terms_of_use - Any license information or restrictions regarding the content. In the Dutch interface: "Gebruiksvoorwaarden"
# E.g. 'FOR INTERNAL USE ONLY'
service_terms_of_use = 'FOR INTERNAL USE ONLY'
# service_credits - Information on the source of the content. In the Dutch interface: "Credits (toeschrijving)"
# E.g. '© Me, myself and I'
service_credits = '© Me, myself and I'
# service_tags - Tags listed as comma-separated values, or a list of strings. Used for searches on items. In the Dutch interface: "Labels"
# E.g. ['INSPIRE','Open Data']
service_tags = ['INSPIRE','Open Data']
# service_wkid - To set the targetSR to the SR of your input data.
# If you don't specify the targetSR data will be transformed to wkid 102100 (-> wkid 3857 -> Web Mercator)
# E.g. 28992 (i.e. RD_New)
service_wkid = 28992
# service_thumbnail_path - The path to a thumbnail file (a 600*400 pixels PNG file) for your service
# E.g.'C:/Data/Thumbnail_test.png'
service_thumbnail_path = ''
# =========================================================================================================================================

print('===================')
print(str(datetime.datetime.now()) + ' - Start')
print('First you have to log in to ArcGIS Online')

# Log in
username, password = provide_credentials()
my_agol = GIS("https://www.arcgis.com", username, password)
del password # It is best to remove the password from memory asap

# Add input File Geodatabase
filegdb = my_agol.content.add({"type" : "File Geodatabase"}, data)
print(str(datetime.datetime.now()) + " - Input FGDB has been added to content on ArcGIS Online")
wait = input("Optionally: check your content - PRESS ENTER TO CONTINUE")

# Publish the FeatureServer
srv_publish_parameters = {'name' : service_name,
                         'description' : service_description,
                         'copyrightText' : service_credits,
                         'targetSR' : { 'wkid' : service_wkid }} 

published_service = filegdb.publish(publish_parameters=srv_publish_parameters)
item_id = published_service.id

print(str(datetime.datetime.now()) + " - Service has been published on ArcGIS Online")
print(str(datetime.datetime.now()) + " - The ItemID of the new service is: {}".format(item_id))
wait = input("Optionally: check your content - PRESS ENTER TO CONTINUE")

# Update description of the service item
item_properties = {'snippet' : service_snippet,
                   'title' : service_name,
                   'description' : service_description,
                   'licenseInfo' : service_terms_of_use,
                   'accessInformation' : service_credits,
                   'tags' : service_tags}

if published_service.update(item_properties, thumbnail=service_thumbnail_path):
    print(str(datetime.datetime.now()) + " - The item properties and the thumbnail of the published service have been updated")
wait = input("Optionally: check your content - PRESS ENTER TO CONTINUE")

# Remove the input File Geodatabase from ArcGIS Online (as it is no longer needed)
if my_agol.content.delete_items([filegdb]):
    print(str(datetime.datetime.now()) + " - The input FGDB has been deleted from the content on ArcGIS Online")

print('===================')
print(str(datetime.datetime.now()) + " - Your Feature Layer has been published")
print('===================')
