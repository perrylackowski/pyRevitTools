"""
Sync ProjectInformation Parameters with CSV file located here:
\\13-0 Design Documents & Lists\\13-2 Design Files\\01 Standards\\TitleBlockParameters.csv

or here:
\\13-0 Design Documents & Lists\\13-2 Drawings\\00 stds\\TitleBlockParameters.csv

TESTED REVIT API: 2020

Author: Robert Perry Lackowski

"""

from Autodesk.Revit.DB import *
from pyrevit import script
import sys

# from pyrevit import DB
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

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

print "\r\n Appending path to project's TitleBlockParameters CSV file..."
csv_file_path = project_folder_path + "\\13-0 Design Documents & Lists\\13-2 Design Files\\01 Standards\\TitleBlockParameters.csv"
print csv_file_path


#csv_file_path = "C:/Users/rpl/Downloads/TitleBlockParameters.csv"
#if os.path.isfile(csv_file_path):
import os.path as op
if op.isfile(csv_file_path):
    print "\r\n Attempting to retrieve parameters..."
    csv_data = script.load_csv(csv_file_path)
else:
    print "\r\n Path is not valid. Trying old path:" 
    csv_file_path = project_folder_path + "\\13-0 Design Documents & Lists\\13-2 Drawings\\00 stds\\TitleBlockParameters.csv"
    print csv_file_path
    if op.isfile(csv_file_path):
        csv_data = script.load_csv(csv_file_path)
    else:
        print "\r\n Path is not valid. Stopping script."
        sys.exit()

print "\r\nParameters retrieved. Beginning to update matching parameters in current project..."

# for row in csv_data:
    # for col in row:
        # print col

project_info = doc.ProjectInformation

t = Transaction(doc)
t.Start('Update Title Block Parameters')

for row in csv_data:
    if row and row[0] != "": #this skips empty rows in the .csv
        
        search_param = row[0]
        
        desired_param_string = ", ".join(row[1::]) #the same as saying row[1], but joins any additional columns (for example, if someone puts "westlake, OH", this will merge the two columns back together)
        
        found_param = project_info.LookupParameter(search_param)
       
        if found_param:
            if found_param.StorageType == StorageType.String:
                if found_param.Set(desired_param_string):
                    print "Parameter \"" + search_param + "\" set to " + found_param.AsString()
                else:
                    print "Found \"" + search_param + "\" parameter, but unable to set its value."
            else:
                print "Found \"" + search_param + "\" parameter, but parameter was not a string type, so its value cannot be modified with this script."
        else:
            print "Could not find \"" + search_param + "\" project information parameter."
        
#doc2.Close()

t.Commit()






