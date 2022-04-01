"""
If a view appears on one or more sheet, the sheet numbers will be appended to the view name in the project browser (for ease of sorting/organizing).

WARNING: If the Title On Sheet parameters are not set for every view, the updated view names may appear on your printed sheets as part of the view title.

TESTED REVIT API: 2020

Author: Robert Perry Lackowski

"""

import view_name_functions #custom script in the lib folder (one folder up from the pushbutton folder)
from Autodesk.Revit.DB import Transaction
doc = __revit__.ActiveUIDocument.Document

t = Transaction(doc)
t.Start('Remove Sheet Numbers from View Names')

view_name_functions.remove_sheet_numbers(doc)
view_name_functions.append_sheet_numbers(doc)

t.Commit()