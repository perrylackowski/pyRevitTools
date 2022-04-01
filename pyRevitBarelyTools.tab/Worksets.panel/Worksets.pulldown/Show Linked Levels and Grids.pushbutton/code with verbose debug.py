'''
Goes to Manage > Manage Links > Manage Worksets and opens the Shared Levels and Grids workset on each link.

TESTED REVIT API: 2020

Author: Robert Perry Lackowski

'''
from pyrevit import DB
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.DB import WorksharingUtils
from Autodesk.Revit.DB import WorksetConfiguration
from Autodesk.Revit.DB import RevitLinkType
from Autodesk.Revit.UI import TaskDialog

from pyrevit import script
output = script.get_output()

import traceback

doc = __revit__.ActiveUIDocument.Document
app = __revit__.ActiveUIDocument.Application.Application

# Set the name of the workset you would like to hide. Decide if you want to hide it or unhide it.
hide_this_workset = "Shared Levels and Grids"
hide_workset = False

for link_doc in app.Documents:
    
    link_doc_title = link_doc.Title
    print link_doc_title

    #this excludes the project file itself
    if not link_doc.IsLinked:
        print "this one isn't linked, skip the rest of the for loop \n\n "
        continue
    
    #This gets a list of the RevitLinkType elements in the active document.
    revit_link_types = FilteredElementCollector(doc).OfClass(DB.RevitLinkType).ToElements()
 
    # This finds the RevitLinkType element that matches the link_doc.
    rlt = next((rlt for rlt in revit_link_types if rlt.LookupParameter("Type Name").AsString().rstrip(".rvt") == link_doc_title), None)
    if not rlt:
        print "No matching RevitLinkType for the link_doc."
    else:
        temp = "Update workset visibility on this file: " + str(link_doc.Title)
        print temp

        # generate a list of the worksets in the link_doc
        workset_table = link_doc.GetWorksetTable()
        model_path = link_doc.GetWorksharingCentralModelPath()
        lst_preview = WorksharingUtils.GetUserWorksetInfo(model_path)

        open_this_list_of_worksets = []
        
        for objWorksetPreview in lst_preview:
            wkset = workset_table.GetWorkset(objWorksetPreview.Id)
            
            temp = wkset.Name + " is open: " + str(wkset.IsOpen)
            print temp
            
            print wkset.Name == hide_this_workset
           
            if hide_workset:
                #gather a list of all the open worksets, EXCLUDING the workset we want to hide
                if wkset.IsOpen and (wkset.Name != hide_this_workset):
                    print "open this one"
                    open_this_list_of_worksets.append(wkset.Id)
            else:
                #gather a list of all the open worksets, INCLUDING the one we hid.
                if wkset.IsOpen or wkset.Name == hide_this_workset:
                    print "open this one v2"
                    open_this_list_of_worksets.append(wkset.Id)
                    
                    
        # print "closing all worksets, then opening the following worksets:"
        # for workset in open_this_list_of_worksets:
            # print workset
        
        # Set the WorksetConfiguration file to close all worksets, then open the ones from the list
        workset_config = WorksetConfiguration(WorksetConfigurationOption.CloseAllWorksets)
        workset_config.Open(open_this_list_of_worksets)
        
        rlt.LoadFrom(model_path, workset_config)
        
        workset_config.Dispose()

print "Script complete."


    
 





