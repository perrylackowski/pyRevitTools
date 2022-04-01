"""
Hide Civil Layers

Finds any CAD imports in the active view and hides unneeded civil layers like contours and text.

TESTED REVIT API: 2020.2.4

Author: Robert Perry Lackowski

"""

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.Attributes import *

doc = __revit__.ActiveUIDocument.Document
app = __revit__.ActiveUIDocument.Application.Application
view = doc.ActiveView;

#list of layers to be hidden. Will find partial matches. Not case-sensitive.
bad_layers = [
"ATR",
"CONTOUR",
"DEMO",
"NO_PLOT",
"TEXT",
"BD_X_TEXT",
"BD_P_BUILDING",
"BR_X_SV_RAIL_TEXT",
"C-ANNO-TEXT",
"DR_X_TEXT",
"DR_P_DRAINAGE_AREA",
"DT_P_SPOT_GRADE",
"DT_P_USER_LABEL",
"DT_X_BREAK_LINE",
"DT_X_SPOT_ELEV",
"DV_X_TEXT",
"G-ANNO-TEXT",
"G-TEXT",
"GT_INSTRUMENTED_CELLS",
"GT_PROJECT_SOIL_BORING",
"GT_X_WELLS_TEXT",
#"LT_P_POLES",
#"PV_P_EOP",
"PV_P_EOP_HATCH",
"PV_X_TEXT",
"RD_X_TEXT",
"RW_X_TEXT",
"SH_TEXT",
"SN_X_TEXT",
"SV_X_SHOT_MARKER",
"SV_X_TEXT",
"UT_X_ELECTRIC_TEXT",
"UT_X_GAS_TEXT",
"UT_X_SANITARY_TEXT",
"UT_X_TELECOM_TEXT",
"UT_X_WATER_TEXT",
"VG_P_LANDSCAPE_LIMITS",
"VG_X_TEXT",
]

#Converts all strings to upper case, and replaces all dashes and spaces with underscores.
bad_layers = map(lambda x:x.upper().replace(" ","_").replace("-","_"), bad_layers)

t = Transaction(doc)
t.Start('Hide Civil CAD Layers')

for category in view.Document.Settings.Categories:
    
    if ".dwg" in category.Name:
    
        try:
            #list of all subcategories. In this case, the subcategories of a drawing are the layers.
            layer_subcats = category.SubCategories

            #hide bad layers
            for layer_cat in layer_subcats:

                layer_cat_name = layer_cat.Name.upper().replace(" ", "_").replace("-", "_")
                #print layer_cat_name
                
                for bad_string in bad_layers:
                    
                    #if-in syntax performs a string matching search
                    if bad_string in layer_cat_name:

                        #print "match found"
                        if view.CanCategoryBeHidden(layer_cat.Id):
                            layer_cat.set_Visible(view, False)
                        #else:
                            #print "couldn't hide"
                        break

        except:
            #print "Exception: Found " + category.Name + " but could not update."
            pass
        
t.Commit()




