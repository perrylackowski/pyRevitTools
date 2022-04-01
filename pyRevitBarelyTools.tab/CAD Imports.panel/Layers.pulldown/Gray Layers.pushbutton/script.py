"""
Gray Layers

Finds any CAD imports in the active view and sets their graphic overrides to gray.

TESTED REVIT API: 2020.2.4

Author: Robert Perry Lackowski

"""

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.Attributes import *

doc = __revit__.ActiveUIDocument.Document
app = __revit__.ActiveUIDocument.Application.Application
view = doc.ActiveView;

t = Transaction(doc)
t.Start('Gray Layers')

gray_color = Color(192, 192, 192)

for category in view.Document.Settings.Categories:
    
    if ".dwg" in category.Name:
        #print category.Name
        
        #list of all subcategories. In this case, the subcategories of a drawing are the layers.
        layer_subcats = category.SubCategories
        
        try:
        
            #create a new override graphic settings object
            override_graphic_settings = OverrideGraphicSettings()
            
            #set the color of the object
            override_graphic_settings.SetProjectionLineColor(gray_color)

            #set each layer to gray by assigning the override graphic settings object
            for layer_cat in layer_subcats:
                view.SetCategoryOverrides(layer_cat.Id,override_graphic_settings)

            #updating line color overrides doesn't update on the screen until you toggle the drawing's visibility like so:
            if category.AllowsVisibilityControl:
                category.set_Visible(view, False)
                category.set_Visible(view, True)
                
        except:
            #print "Exception: Found " + category.Name + " but could not update."
            pass

t.Commit()




