"""
Pushes elements to the appropriate Worksets, creating worksets if they do not exist:

Levels -> Shared Levels and Grids
Grids -> Shared Levels and Grids
Reference Planes -> Shared Levels and Grids
Match Lines -> Match Lines
Scope Boxes -> Other Model Content
Lighting Calc Tools -> Other Model Content

TESTED REVIT API: 2020

Author: Robert Perry Lackowski

"""

from pyrevit import script, revit, DB
from Autodesk.Revit.DB import Workset, Transaction, FilteredWorksetCollector, WorksetKind, FilteredElementCollector, BuiltInParameter, BuiltInCategory
from Autodesk.Revit.UI import TaskDialog

output = script.get_output()

doc = __revit__.ActiveUIDocument.Document


def GetWorksetIdInt(targetWorksetName):
    
    workset_collector = FilteredWorksetCollector(doc).OfKind(WorksetKind.UserWorkset)
    
    #find target workset
    workset = next((ws for ws in workset_collector if ws.Name == targetWorksetName), None)

    #if it does not exist, create a new one
    if not workset:
        print ". Workset \"" + targetWorksetName + "\" does not exist in project. Adding workset."
        workset = Workset.Create(doc, targetWorksetName)

    return workset.Id.IntegerValue


def UpdateWorkset(e, desired_workset_id_int):
    # try:
        e_workset_id = e.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
        e_workset_id.Set(desired_workset_id_int)
        try:
            temp = ". " + e.Category.Name + ", " + e.Symbol.Family.Name + ", " + e.Name + " " + output.linkify(e.Id)
            print temp
        except:
            try:
                temp = ". " + e.Category.Name + ", " + e.Name + output.linkify(e.Id)
                print temp
            except:
                try:
                    temp = e.Name + ", " + output.linkify(e.Id)
                    print temp
                except:
                    try:
                        temp = output.linkify(e.Id)
                        print temp
                    except:
                        print "updated workset, but couldn't create link for element"
                    
    # except:
        # print "excepted"
        # pass

groups_to_update = []

groups_to_update.append(["Levels","Shared Levels and Grids", FilteredElementCollector(doc).WhereElementIsNotElementType().OfClass(DB.Level).ToElements()]) #levels
groups_to_update.append(["Grids","Shared Levels and Grids", FilteredElementCollector(doc).WhereElementIsNotElementType().OfClass(DB.Grid).ToElements()]) #grids
groups_to_update.append(["Reference Planes","Shared Levels and Grids", FilteredElementCollector(doc).WhereElementIsNotElementType().OfCategory(BuiltInCategory.OST_CLines).ToElements()]) #reference_planes
groups_to_update.append(["Match Lines","Match Lines", FilteredElementCollector(doc).WhereElementIsNotElementType().OfCategory(BuiltInCategory.OST_Matchline).ToElements()]) # Matchlines
groups_to_update.append(["Scope Boxes","Other Model Content", FilteredElementCollector(doc).WhereElementIsNotElementType().OfCategory(BuiltInCategory.OST_VolumeOfInterest).ToElements()]) #scope_boxes
groups_to_update.append(["Spaces","Other Model Content", FilteredElementCollector(doc).WhereElementIsNotElementType().OfCategory(BuiltInCategory.OST_MEPSpaces).ToElements()]) #spaces
groups_to_update.append(["Space Separation Lines","Other Model Content", FilteredElementCollector(doc).WhereElementIsNotElementType().OfCategory(BuiltInCategory.OST_MEPSpaceSeparationLines).ToElements()]) #space_separation_lines


#since we don't want to put ALL the generic_models on the Other Model Content workset, we use Python's list comprehensions to further filter the FEC:
generic_models = FilteredElementCollector(doc).WhereElementIsNotElementType().OfCategory(BuiltInCategory.OST_GenericModel).ToElements()
groups_to_update.append(["ElumTools Calc Points","Other Model Content", [e for e in generic_models if ("ElumTools" in e.Symbol.Family.Name)]]) #ElumTools lighting families. Family Name must contain ElumTools
groups_to_update.append(["Fixture Spacer Tools","Other Model Content", [e for e in generic_models if ("Fixture Spacer Tool" in e.Name)]]) #Fixture Spacer grid lines families. Type Name must contain ElumTools

#since we don't want ALL mechanical equipment on the Other Model Content workset, we repeat for power taps.
electrical_fixtures = FilteredElementCollector(doc).WhereElementIsNotElementType().OfCategory(BuiltInCategory.OST_ElectricalFixtures).ToElements()
groups_to_update.append(["REW Electrical Fixture Power Taps","Other Model Content", [e for e in electrical_fixtures if ("Power Tap" in e.Symbol.Family.Name)]]) #REW EF Power Tap families. Family Name must contain REW EF Power Tap

if doc.IsWorkshared:
    t = Transaction(doc)
    t.Start('Push to Worksets')

    for group in groups_to_update:
        print "\nGroup: " + group[0] + " -> " + group[1]
        
        #list comprehension to exclude elements that don't have an accessible Workset parameter.
        try:
            elems = [e for e in group[2] if e.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM).IsReadOnly == False]
        except:
            print "Skipping " + group[0] + " because it contains elements which do not contain the Workset parameter."
            continue
        
        print ".  Element count: " + str(len(elems)) #technicallly this is the element count AFTER excluding items with read-only worksets, but most users won't know what that means
        
        if elems: #if there are still elements in the FilteredElementCollector list, proceed.
            
            # at this point it's safe to retrieve or create a workset ID which matches the string, since we need to compare it to the existing worksets.
            workset_id_int = GetWorksetIdInt(group[1])

            #another list comprehension, cutting the list down to only include elements which are on the incorrect workset.
            elems = [e for e in elems if e.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM).AsInteger() != workset_id_int]
            
            if elems: #if the list still contains elements, we can notify the user we are going to update:
                print ".  Moving " + str(len(elems)) + " " + group[0] + " to \"" + group[1] + "\" Workset:"
                for e in elems:
                    UpdateWorkset(e,workset_id_int)
            else:
                print ".  All elements are on the correct workset."
        else:
            print ".  No elements to modify."
    
    t.Commit()
else:
    print "Project is not workshared. Enable collaboration, or use the Add Worksets tool first.", "\n\n"
    
print "\nScript complete."

# print "Reasons an element may fail to update:"
# print "1. Elements may be grouped"
# print "2. Elements may be on a non-user-created workset (for example, reference planes in a drafting view)"
# print "3. Elements may be shared/nested in other families"
