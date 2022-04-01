'''
Enables worksharing, and adds the following worksets:
["Shared Levels and Grids","Workset1"]['LINK-A','LINK-C','LINK-E','LINK-M','LINK-P','LINK-S','LINK-CAD','Match Lines','Other Model Content']

TESTED REVIT API: 2020

Author: Robert Perry Lackowski

'''

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import Workset, Transaction
from Autodesk.Revit.DB import FilteredWorksetCollector, WorksetKind
from Autodesk.Revit.DB import Document

doc = __revit__.ActiveUIDocument.Document

#list of worksets to add to project
list_worksets_new = ['LINK-A','LINK-C','LINK-E','LINK-M','LINK-P','LINK-S','LINK-CAD','LINK-GRID', 'Match Lines','Other Model Content']

#enable worksharing
if not doc.IsWorkshared:
    print "Project is not workshared. Enabling local worksharing now.", "\n\n"
    doc.EnableWorksharing("Shared Levels and Grids","Workset1")
    
print "Worksharing enabled, clear to proceed.", "\n\n"
    
print "This tool will attempt to add the following list of worksets to the project: ", list_worksets_new, "\n\n"

# get list of workset names
worksets = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets()
list_worksets_existing = []
for workset in worksets:
	list_worksets_existing.append(workset.Name)

print "Existing worksets: ", list_worksets_existing, "\n\n"

#remove redundant names
for element in list_worksets_existing:
    if element in list_worksets_new:
        list_worksets_new.remove(element)

print "Worksets still missing from your project:", list_worksets_new, "\n\n"

#add missing worksets
t = Transaction(doc)
t.Start('Create Worksets')
for workset_name in list_worksets_new:
    Workset.Create(doc, workset_name)
t.Commit()

# get list of workset names again
worksets = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset).ToWorksets()
list_worksets_final = []
for workset in worksets:
	list_worksets_final.append(workset.Name)

print "Updated list of worksets: ", list_worksets_final, "\n\n"






















