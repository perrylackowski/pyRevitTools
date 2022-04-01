"""
Wipe Line Styles from searchable checklist.

If you remove a line style, any lines using that style will have their style set to Thin Lines.
You may not remove built-in line styles.

TESTED REVIT API: 2020

Author: Robert Perry Lackowski
"""

from Autodesk.Revit.DB import BuiltInCategory, Transaction
from pyrevit import forms, DB

doc = __revit__.ActiveUIDocument.Document

#Put all the line styles in a list
line_category = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Lines)
collector = line_category.SubCategories

#Generate a list of the line style names
names = [element.Name for element in collector]
names.sort()

#Remove all of Revit's built-in names which contain <brackets>
names = [n for n in names if "<" not in n]

#Remove built in names from names list:
default_names = ["Axis of Rotation", "Hidden Lines", "Insulation Batting Lines", "Lines", "Medium Lines", "Path of Travel Lines", "Thin Lines", "Wide Lines"]
names = [n for n in names if n not in default_names]

#ask the user to select which line styles they want to remove
chosen_names = forms.SelectFromList.show(names, multiselect = True, button_name = 'Remove')

if chosen_names:

    #convert the list of names back to a list of line styles
    chosen_elements = [element for element in collector if element.Name in chosen_names]

    t = Transaction(doc, "Remove Line Styles")
    t.Start()
    for element in chosen_elements:
        doc.Delete(element.Id)
    t.Commit()
    
    msg = "Line Styles Removed:\n"
    for name in chosen_names:
        msg += ("{}\n".format(name))
    
    forms.alert(msg,title='Line Styles Remover', ok=True)