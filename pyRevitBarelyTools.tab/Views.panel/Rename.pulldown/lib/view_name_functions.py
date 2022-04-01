split_string = "--"
from pyrevit import DB
from Autodesk.Revit.DB import *

def remove_sheet_numbers(doc):
    view_FEC = FilteredElementCollector(doc).WhereElementIsNotElementType().OfCategory(BuiltInCategory.OST_Views).ToElements()
    # schedule_FEC = FilteredElementCollector(doc).WhereElementIsNotElementType().OfCategory(BuiltInCategory.OST_Schedules).ToElements()
    # panel_schedule_FEC = FilteredElementCollector(doc).WhereElementIsNotElementType().OfCategory(BuiltInCategory.OST_PanelScheduleGraphics).ToElements()
    # schedule FEC will include schedules, but it will also include revision schedules.
    #OST_PanelScheduleGraphics won't doesn't get panel schedules...
    
    def remove_sheet_numbers_in_set(FEC_set):
        for view in FEC_set:
            view_name = view.Name
            # print view_name
            if split_string in view_name:
                # print view_name
                shortened_name = view_name[view_name.find(split_string):][len(split_string)::] #Removes all characters before and including the first split_string.
                # print shortened_name
                try:
                    view.Name = shortened_name
                except:
                    print "Unable to update all the view names. Could not shorten \"" + view_name + "\" to \"" + shortened_name + "\". Shortened name may already appear in the project."
                # print "UPDATED: " + view.Name

    remove_sheet_numbers_in_set(view_FEC)
    # remove_sheet_numbers_in_set(schedule_FEC)
    # remove_sheet_numbers_in_set(panel_schedule_FEC)
    

def append_sheet_numbers(doc):
    sheets_FEC = FilteredElementCollector(doc).WhereElementIsNotElementType().OfClass(DB.ViewSheet).ToElements()

    #create a list of views that appear on sheets, with lists of sheet numbers that they appear on.
    views_to_update = []
    #example of final data
    # [
    #   [View1_ID,['E100','E101','E102']],
    #   [View2_ID,['E100','E101','E102']],
    #   [View3_ID,['S603']],
    # ]

    for sheet in sheets_FEC:
        
        # print sheet.Name
        # print sheet.SheetNumber
        
        views_on_sheet = sheet.GetAllPlacedViews() #gets a list of the View Ids
        # schedules_on_sheet = FilteredElementCollector(doc,sheet.Id).
        
        for view_id in views_on_sheet: 
            
            view_in_update_list = False
            
            for view in views_to_update: #search through views_to_update and append a sheet number if the view_id row already exists
                
                if view_id == view[0]:
                    
                    view[1].append(sheet.SheetNumber)
                    view_in_update_list = True
                    break
                    
            if view_in_update_list == False: #if it does not exist, append a new view_id row
                
                views_to_update.append([view_id,[sheet.SheetNumber]])


    for view in views_to_update:
        
        view[1].sort() #alphabetize the sheet number strings for each view_id
        
        # print view[1]

        view[1] = ', '.join(view[1]) #merge the sheet number strings into a single comma separated string

    # print views_to_update


    for view in views_to_update:
        
        view_elem = doc.GetElement(view[0])
        
        if view_elem:
            view_elem.Name = view[1] + split_string + view_elem.Name

