"""
Restore Layers

Finds any CAD imports in the active view and restores their original colors and visibility.

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
t.Start('Restore Layers')


for category in view.Document.Settings.Categories:
    
    if ".dwg" in category.Name:
        #print category.Name

        try:
        
            #list of all subcategories. In this case, the subcategories of a drawing are the layers.
            layer_subcats = category.SubCategories
        
            #create an override graphic settings object with default settings
            override_graphic_settings = OverrideGraphicSettings()

            for layer_cat in layer_subcats:
                
                print layer_cat.Name
                
                #assign default override graphics object
                view.SetCategoryOverrides(layer_cat.Id,override_graphic_settings)
            
                #restore visibility
                if view.CanCategoryBeHidden(layer_cat.Id):
                    layer_cat.set_Visible(view, True)

            #updating line color overrides doesn't update on the screen until you toggle the drawing's visibility, like so:
            if category.AllowsVisibilityControl:
                category.set_Visible(view, False)
                category.set_Visible(view, True)
                
        except:
            #print "Exception: Found " + category.Name + " but could not update."
            pass

t.Commit()

