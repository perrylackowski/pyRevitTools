'''
Exports a Navisworks NWC file to the 
[#####]\\20-0 Internal Reviews\\20.3_Navisworks\\
subdirectory that matches the project number of the active file.

Script will export the \"Navisworks Export View\" 3D view if it can find it. Otherwise it will export everything.
Exported file name will match project file name.
Script will open directory where file has been saved.

TESTED REVIT API: 2020

Author: Robert Perry Lackowski

'''

from pyrevit import DB
from pyrevit import script
from Autodesk.Revit.DB import FilteredElementCollector, NavisworksExportOptions, NavisworksExportScope
from Autodesk.Revit.DB import Document
from Autodesk.Revit.DB import INavisworksExporter, NavisworksExportOptions, OptionalFunctionalityUtils, ModelPathUtils

doc = __revit__.ActiveUIDocument.Document

import sys
if not OptionalFunctionalityUtils.IsNavisworksExporterAvailable():
    print "Navisworks Exporter Utility is not installed. Utility is required to run this script. Downloads available here (as of 2021):"
    
    output = script.get_output()
    output.print_html('<a href="https://www.autodesk.com/products/navisworks/3d-viewers">Navisworks Exporter Utility</a>')
    sys.exit()

#Find the view you want to export using the view names
def GetExportView(view_name):
    view_collector = FilteredElementCollector(doc).OfClass(DB.View)
    for view_element in view_collector:
        if view_element.Name == view_name:
            return view_element.Id
    return None

#assign the result
view_id = GetExportView("Navisworks Export View")

#create a default export option
navisworks_export_options = NavisworksExportOptions()

#if an appropriate view is found, update the export option to use the view.
if view_id:
    output = script.get_output()
    temp = "Navisworks Export View found in project. Exporting as an NWC: " + output.linkify(view_id)
    navisworks_export_options.ExportScope = NavisworksExportScope.View
    navisworks_export_options.ViewId = view_id
    print temp
else:
    print "Could not find a 3D view named \"Navisworks Export View\". Exporting entire contents of file instead."



print "\r\n Retreiving central file path..."

def GetCentralServerPath(doc):
    modelPath = doc.GetWorksharingCentralModelPath()
    centralServerPath = ModelPathUtils.ConvertModelPathToUserVisiblePath(modelPath)
    return centralServerPath
    
central_file_path = GetCentralServerPath(doc)

print central_file_path

print "\r\n Splitting text string to retreive the project folder..."

#match the entire path up to the first 5 digit # from the left.
import re
regular_expression = ".+?(?=\d{5})\d{5}"
x = re.search(regular_expression, central_file_path)
if x:
    project_folder_path = x.group()
    print project_folder_path
else:
    print "No 5 digit project number found in string. No file has been exported."
    sys.exit()

print "\r\n Appending path to project's Navisworks folder..."
project_folder_path = project_folder_path + "\\20-0 Internal Reviews\\20.3_Navisworks\\"
print project_folder_path

print "\r\n Appending project name..."
project_name = central_file_path[central_file_path.rindex("\\"):]
project_name = project_name[1:(len(project_name)-4)]
print project_folder_path + project_name

print "\r\n Attempting to export navisworks file..."
Document.Export(doc, project_folder_path, project_name, navisworks_export_options)
print "\r\nExport complete. Opening folder..."

import subprocess
command = r'explorer ' + "\"" + project_folder_path + "\""
subprocess.Popen(command)

#format should be like this: 
#subprocess.Popen(r'explorer "C:\Users\rpl\Documents\your folder"')



















