"""
Wipe Line Patterns from searchable checklist.

If you remove a line pattern, any line styles or categories using that pattern will have their pattern set to Solid.

TESTED REVIT API: 2020

Author: Robert Perry Lackowski
"""

from Autodesk.Revit.DB import BuiltInCategory, Transaction, FilteredElementCollector
from pyrevit import forms, DB

doc = __revit__.ActiveUIDocument.Document

#Put all the line patterns in a list
collector = FilteredElementCollector(doc).OfClass(DB.LinePatternElement).ToElements()

#Generate a list of the line pattern names
names = [element.Name for element in collector]
names.sort()

#Ask the user to select which line styles they want to remove
chosen_names = forms.SelectFromList.show(names, multiselect = True, button_name = 'Remove')

if chosen_names:

    #convert the list of names back to a list of line patterns    
    chosen_elements = [element for element in collector if element.Name in chosen_names]

    t = Transaction(doc, "Remove Line Patterns")
    t.Start()
    for element in chosen_elements:
        doc.Delete(element.Id)
    t.Commit()
    
    msg = "Line Patterns Removed:\n"
    for name in chosen_names:
        msg += ("{}\n".format(name))
    
    forms.alert(msg,title='Line Pattern Remover', ok=True)

