from pyrevit import revit, DB
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, LinkedFileStatus, WorksharingUtils, WorksetConfiguration, WorksetConfigurationOption

doc = __revit__.ActiveUIDocument.Document

def update_worksets(update_these_worksets, show_workset):    

    revit_link_types = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RvtLinks).OfClass(DB.RevitLinkType).ToElements()
    revit_link_instances = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RvtLinks).OfClass(DB.RevitLinkInstance)
    for link_type in revit_link_types:

        print "\nLink: " + link_type.LookupParameter("Type Name").AsString()
        
        if link_type.GetLinkedFileStatus() == LinkedFileStatus.Loaded:

            link_instance = list(filter(lambda x: (x.GetTypeId() == link_type.Id), revit_link_instances))[0]        
            link_document = link_instance.GetLinkDocument()
            
            #generate a list of the worksets in the link_document
            workset_table = link_document.GetWorksetTable()
            model_path = link_document.GetWorksharingCentralModelPath()
            lst_preview = WorksharingUtils.GetUserWorksetInfo(model_path)

            # initialize list of worksets to enable
            open_this_list_of_worksets = []
            
            for objWorksetPreview in lst_preview:
                wkset = workset_table.GetWorkset(objWorksetPreview.Id)
                temp = ".  " + wkset.Name + " - "
                if show_workset:
                    #gather a list of all the open worksets, INCLUDING the ones we hid.
                    if wkset.IsOpen or (wkset.Name in update_these_worksets):
                        open_this_list_of_worksets.append(wkset.Id)
                        if wkset.IsOpen:
                            temp = temp + "Loaded"
                        else:
                            temp = temp + "Loading now"
                    else:
                        if wkset.IsOpen:
                            temp = temp + "Unloading now"
                        else:
                            temp = temp + "Unloaded"
                else:
                    #gather a list of all the open worksets, EXCLUDING the worksets we want to hide
                    if wkset.IsOpen and not (wkset.Name in update_these_worksets):
                        open_this_list_of_worksets.append(wkset.Id)
                        if wkset.IsOpen:
                            temp = temp + "Loaded"
                        else:
                            temp = temp + "Loading now"
                    else:
                        if wkset.IsOpen:
                            temp = temp + "Unloading now"
                        else:
                            temp = temp + "Unloaded"

                print temp
                
            # Set the WorksetConfiguration file to close all worksets, then open the ones from the list
            workset_config = WorksetConfiguration(WorksetConfigurationOption.CloseAllWorksets)
            workset_config.Open(open_this_list_of_worksets)
            
            #reload the link with the updated workset configuration
            link_type.LoadFrom(model_path, workset_config) #FAILS WHEN LINK IS LINKED INTO TWO OPEN FILES. WORKS THROUGH UI THOUGH...
            
            #delete the workset configuration after use
            workset_config.Dispose()
    
    
    
    
    
    
    
    
    
    
