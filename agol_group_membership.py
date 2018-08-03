## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## ArcGIS Online Management Information
## Script: agol_group_membership.py
## Goal: to create an overview of group membership in your ArcGIS Online organisation
## Author: Egge-Jan Polle - Tensing GIS Consultancy
## Date: August 3, 2018
## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# This script should be run within a specific ArcGIS/Python environment using the batch file below
# (This batch file comes with the installation of ArcGIS Pro)
# "C:\Program Files\ArcGIS\Pro\bin\Python\scripts\propy.bat" agol_group_membership.py
#
import csv,os, sys
from arcgis.gis import GIS
from provide_credentials import provide_credentials

print('===================')
print('The script that is running: ' + __file__)
print('First you have to log in to ArcGIS Online')

# Log in
username, password = provide_credentials()
my_agol = GIS("https://www.arcgis.com", username, password)

print ("Start: "+datetime.datetime.today().strftime('%c'))

## Get all groups
my_groups = my_agol.groups.search()
## Optionally: have a look at all groups
#my_groups
## Optionally: count the number of groups
#len(my_groups)

## Get all users
my_users = my_agol.users.search(max_users = 350) # The default of max_users = 100, so increase it if you have more
## Optionally: have a look at all users
#my_users
## Optionally: count the number of users
#len(my_users)

## Create a list with all group titles
my_group_titles = []
for my_group in my_groups:
    my_group_titles.append(my_group.title)

## Create a list with field names
fieldnames = []
fieldnames = ['USERNAME','EMAIL']
for title in my_group_titles:
    fieldnames.append(title)
## Optionally: have a look at the field names
#fieldnames

## Create a CSV file with a matrix of the groups with their members
today = datetime.datetime.today().strftime('%Y%m%d')
fname = 'AGOL_Group_Membership'+today+'.csv'
try:
    os.remove(fname)
except OSError:
    pass
outfile = open(fname, 'a')
writer = csv.DictWriter(outfile, delimiter = ';', lineterminator='\n', fieldnames=fieldnames)
writer.writeheader()
## Add for each user the full name and email and for each group a 1 or 0, depending on group membership
for user in my_users:
    membership = []
    try:
        thisUser = {}
        thisUser['USERNAME'] = user.fullName
        thisUser['EMAIL'] = user.email
        
        try: # Group membership outside the organisation will raise an error ("You do not have permissions to access this resource or perform this operation.")
            for group in user.groups:
                membership.append(group.title)
        except:
            pass
        for title in my_group_titles:
            if title in membership:
                thisUser[title] = 1
            else:
                thisUser[title] = 0
    except:
        print("PLEASE NOTE: no information can be retrieved about user "+user.fullName+".")
        pass
    writer.writerow(thisUser)
outfile.close()
print ("Ready: "+datetime.datetime.today().strftime('%c'))
print()
print('===================')
print('The CSV file can be found here:')
print(os.path.abspath(fname))
print('===================')