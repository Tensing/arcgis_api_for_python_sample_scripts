## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## Script: domain_definitions.py
## Author: Egge-Jan Polle - Tensing GIS Consultancy
## Date: August 9, 2018
## ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import arcpy
def create_domains(gdb):
    
    domain_definitions = [
    ['Status','STATUS_DOMAIN',[
    'Poor','Fair','Good','Very good','Excellent']],
    ['Color','COLOR_DOMAIN',[
    'Red','Green','Yellow','Blue']]
    ]
    
    for domain_definition in domain_definitions:
        arcpy.CreateDomain_management(in_workspace=gdb, domain_name=domain_definition[1], domain_description=domain_definition[0], field_type="TEXT", domain_type="CODED", split_policy="DEFAULT", merge_policy="DEFAULT")
        for value in domain_definition[2]:
            arcpy.AddCodedValueToDomain_management(in_workspace=gdb, domain_name=domain_definition[1], code=value, code_description=value)