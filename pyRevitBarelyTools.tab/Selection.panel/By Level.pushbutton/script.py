"""
Selects all elements that share the same Level as the selected element or Level.

TESTED REVIT API: 2020.2.4

Author: Robert Perry Lackowski

"""

from Autodesk.Revit.DB import ElementLevelFilter, FilteredElementCollector
from Autodesk.Revit.DB import Document, BuiltInParameter, BuiltInCategory, ElementFilter, ElementCategoryFilter, LogicalOrFilter, ElementIsElementTypeFilter, ElementId
from Autodesk.Revit.Exceptions import OperationCanceledException
# from pyrevit import DB
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

from rpw import ui
import sys

#Ask user to pick an object which has the desired reference level
def pick_object():
    from Autodesk.Revit.UI.Selection import ObjectType
    
    try:
        picked_object = uidoc.Selection.PickObject(ObjectType.Element, "Select an element or level.")
        if picked_object:
            return doc.GetElement(picked_object.ElementId)
        else:
            sys.exit()
    except:
        sys.exit()
    
def get_level_id(elem):
        
    BIPs = [
        BuiltInParameter.CURVE_LEVEL,
        BuiltInParameter.DPART_BASE_LEVEL_BY_ORIGINAL,
        BuiltInParameter.DPART_BASE_LEVEL,
        # BuiltInParameter.FABRICATION_LEVEL_PARAM,
        BuiltInParameter.FACEROOF_LEVEL_PARAM,
        BuiltInParameter.FAMILY_BASE_LEVEL_PARAM,
        BuiltInParameter.FAMILY_LEVEL_PARAM,
        BuiltInParameter.GROUP_LEVEL,
        BuiltInParameter.IMPORT_BASE_LEVEL,
        BuiltInParameter.INSTANCE_REFERENCE_LEVEL_PARAM,
        BuiltInParameter.INSTANCE_SCHEDULE_ONLY_LEVEL_PARAM,
        BuiltInParameter.LEVEL_PARAM,
        BuiltInParameter.MULTISTORY_STAIRS_REF_LEVEL,
        BuiltInParameter.PATH_OF_TRAVEL_LEVEL_NAME,
        BuiltInParameter.PLAN_VIEW_LEVEL,
        # BuiltInParameter.RBS_START_LEVEL_PARAM,
        BuiltInParameter.ROOF_BASE_LEVEL_PARAM,
        BuiltInParameter.ROOF_CONSTRAINT_LEVEL_PARAM,
        BuiltInParameter.ROOM_LEVEL_ID,
        BuiltInParameter.SCHEDULE_BASE_LEVEL_PARAM,
        BuiltInParameter.SCHEDULE_LEVEL_PARAM,
        BuiltInParameter.SLOPE_ARROW_LEVEL_END,
        # BuiltInParameter.SPACE_REFERENCE_LEVEL_PARAM,
        BuiltInParameter.STAIRS_BASE_LEVEL,
        BuiltInParameter.STAIRS_BASE_LEVEL_PARAM,
        BuiltInParameter.STAIRS_RAILING_BASE_LEVEL_PARAM,
        BuiltInParameter.STRUCTURAL_REFERENCE_LEVEL_ELEVATION,
        BuiltInParameter.SYSTEM_ZONE_LEVEL_ID,
        BuiltInParameter.TRUSS_ELEMENT_REFERENCE_LEVEL_PARAM,
        BuiltInParameter.VIEW_GRAPH_SCHED_BOTTOM_LEVEL,
        BuiltInParameter.VIEW_UNDERLAY_BOTTOM_ID,
        BuiltInParameter.WALL_BASE_CONSTRAINT,
        BuiltInParameter.WALL_SWEEP_LEVEL_PARAM
        # BuiltInParameter.ZONE_LEVEL_ID,
    ]
    
    level_id = None
        
    for BIP in BIPs:
        param = elem.get_Parameter(BIP)
        if param:
            # print "A common level parameter has been found:" + str(BIP)
            param_elem_id = param.AsElementId()
            if param_elem_id.Compare(ElementId.InvalidElementId) == 1:
                level_id = param_elem_id
                # print "match found on common level parameter " + str(BIP) + "Level ID: " + str(level_id)
                return level_id
    
    # print "No matching common level parameters found, checking for .LevelId"
    try:
        level_id = elem.LevelId
        if level_id.Compare(ElementId.InvalidElementId) == 1:
            # print "match found on .LevelId. Level ID: " + str(level_id)
            return level_id
    except:
        # print "No LevelId parameter on this element."
        pass

    # print "Still no matches. Try checking for .ReferenceLevel.Id"
    
    try:
        level_id = elem.ReferenceLevel.Id
        if level_id.Compare(ElementId.InvalidElementId) == 1:
            # print "match found on .ReferenceLevel.Id Level ID: " + str(level_id)            
            return level_id
    except:
        # print "No ReferenceLevel parameter on this element."
        pass
    
    # print "No matches found. Returning None..."
    return None

# print "get selected element, either from current selection or new selection"
selection = ui.Selection()

if selection:
    selected_element = selection[0]
else:
    selected_element = pick_object()

#print "Element selected: " + selected_element.Name

# print "Check if selected element is a Level and get its ID. If not, search through the parameters for the reference level."
#elem.Category.Id.IntegerValue.Equals( (int) BuiltInCategory.OST_Levels ) is language agnostic version, since "Levels" isn't called levels in every language - for example, it could be "Ebenen" in German
if selected_element.Category.Name.Equals("Levels"):
    target_level_id = selected_element.Id
else:
    target_level_id = get_level_id(selected_element)
    
# print target_level_id

if target_level_id is not None:
    
    #poor attempts at filtering FECs. Not filtered enough - they contain far too many elements.
    #all_elements = FilteredElementCollector(doc).ToElements()
    #all_elements = FilteredElementCollector(doc).WherePasses(LogicalOrFilter(ElementIsElementTypeFilter( False ), ElementIsElementTypeFilter( True ) ) ).ToElements()
    
    #Create a filter. If this script isn't selecting the elements you want, it's possible the category needs to be added to this list.
    BICs = [
        BuiltInCategory.OST_CableTray,
        BuiltInCategory.OST_CableTrayFitting,
        BuiltInCategory.OST_Conduit,
        BuiltInCategory.OST_ConduitFitting,
        BuiltInCategory.OST_DuctCurves,
        BuiltInCategory.OST_DuctFitting,
        BuiltInCategory.OST_DuctTerminal,
        BuiltInCategory.OST_ElectricalEquipment,
        BuiltInCategory.OST_ElectricalFixtures,
        BuiltInCategory.OST_FloorOpening,
        BuiltInCategory.OST_Floors,
        BuiltInCategory.OST_FloorsDefault,
        BuiltInCategory.OST_LightingDevices,
        BuiltInCategory.OST_LightingFixtures,
        BuiltInCategory.OST_MechanicalEquipment,
        BuiltInCategory.OST_PipeCurves,
        BuiltInCategory.OST_PipeFitting,
        BuiltInCategory.OST_PlumbingFixtures,
        BuiltInCategory.OST_RoofOpening,
        BuiltInCategory.OST_Roofs,
        BuiltInCategory.OST_RoofsDefault,
        BuiltInCategory.OST_SpecialityEquipment,
        BuiltInCategory.OST_Sprinklers,
        BuiltInCategory.OST_StructuralStiffener,
        BuiltInCategory.OST_StructuralTruss,
        BuiltInCategory.OST_StructuralColumns,
        BuiltInCategory.OST_StructuralFraming,
        BuiltInCategory.OST_StructuralFramingSystem,
        BuiltInCategory.OST_StructuralFramingOther,
        BuiltInCategory.OST_StructuralFramingOpening,
        BuiltInCategory.OST_StructuralFoundation,
        BuiltInCategory.OST_Walls,
        BuiltInCategory.OST_Wire,
    ]
    
    category_filters = []
    
    for BIC in BICs:
        category_filters.Add(ElementCategoryFilter(BIC))
    
    final_filter = LogicalOrFilter(category_filters)
    
    #Apply filter to create list of elements
    all_elements = FilteredElementCollector(doc).WherePasses(final_filter).WhereElementIsNotElementType().WhereElementIsViewIndependent().ToElements()

    # print "Number of elements that passed collector filters:" + str(len(all_elements))

    selection.clear()

    for elem in all_elements:
        elem_level_id = get_level_id(elem)
        if elem_level_id == target_level_id:
            selection.add(elem)

    selection.update()
    
else:
    
    print "No level associated with element."

