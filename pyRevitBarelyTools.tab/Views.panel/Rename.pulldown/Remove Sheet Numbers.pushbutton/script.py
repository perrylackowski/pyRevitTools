"""
Removes any sheet numbers appended to the front of view names in the project browser.

TESTED REVIT API: 2020

Author: Robert Perry Lackowski

"""



import view_name_functions #custom script in the lib folder (one folder up from the pushbutton folder)
from Autodesk.Revit.DB import Transaction
doc = __revit__.ActiveUIDocument.Document

t = Transaction(doc)
t.Start('Remove Sheet Numbers from View Names')

view_name_functions.remove_sheet_numbers(doc)

t.Commit()