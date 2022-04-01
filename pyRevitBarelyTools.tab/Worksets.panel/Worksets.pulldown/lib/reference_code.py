# print doc.Title
# print "modifiable " + (str)(doc.IsModifiable)
# print "modified " + (str)(doc.IsModified)
# print "readonly " + (str)(doc.IsReadOnly)
# print "readonlyfile " + (str)(doc.IsReadOnlyFile)
# print "IsFamilyDocument " + (str)(doc.IsFamilyDocument)
# print "IsWorkshared " + (str)(doc.IsWorkshared)
# print "IsLinked" + (str)(doc.IsLinked)
# print "\n\n"

# for docu in app.Documents:
    
    # print docu.Title
    # print "modifiable " + (str)(docu.IsModifiable)
    # print "modified " + (str)(docu.IsModified)
    # print "readonly " + (str)(docu.IsReadOnly)
    # print "readonlyfile " + (str)(docu.IsReadOnlyFile)
    # print "IsFamilyDocument " + (str)(docu.IsFamilyDocument)
    # print "IsWorkshared " + (str)(docu.IsWorkshared)
    # print "IsLinked" + (str)(docu.IsLinked)
    # print "\n\n"

# # app.Documents returns a Document Set of all open documents. Each linked file gets a document. The active revit file gets a document.
# # If you have multiple revit projects open, they each get a document. If two open files link in a third file, that file will have ONE document.
# for docu in app.Documents:
    # # If the document is isn't linked, it's one of the open project files, so we skip it. We aren't messing with the worksets on the open project, just the worksets on the linked files.
    # if docu.IsLinked == False:
        # continue

    # # this is a redundant check, that's less effective since it only excludes the active open document/.rvt file, not ALL open documents. Can ignore.
    # # if doc.Title == docu.Title:
        # # continue
    
    # # this finds all the links in the ACTIVE document.
    # revit_link_types = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RvtLinks).OfClass(DB.RevitLinkType).ToElements()
    # rlt = next((rlt for rlt in revit_link_types if rlt.LookupParameter("Type Name").AsString().rstrip(".rvt") == docu.Title), None)
    # if rlt:
        # print "Updating workset visibility on this file: " + str(docu.Title)
        



    # print 
    # IsModifiable - whether the document may be modified
# IsModified - whether the document was changed since it was opened or saved
# IsReadOnly - whether the document is currently read only or can be modified
# IsReadOnlyFile - whether the document was opened in read-only mode
# IsFamilyDocument - whether the document is a family document
# IsWorkshared - whether worksets have been enabled in the document"

    # Exclude the project file itself
    # if not link_doc.IsLinked:
        # print "this one isn't linked, skip the rest of the for loop \n\n "
        # continue
    
    # # Get a list of the RevitLinkType elements in the active document.
    # revit_link_types = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RvtLinks).OfClass(DB.RevitLinkType).ToElements()



# import datatable as dt
# print(dt.__version__)

    # rvtLinks = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RvtLinks).OfClass(DB.RevitLinkType)
    # if (rvtLinks.ToElements().Count > 0):
        
        # for rvtLink in rvtLinks.ToElements():
            
            # if (rvtLink.GetLinkedFileStatus() == LinkedFileStatus.Loaded):
                # print rvtLink.Name
                # link = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_RvtLinks).OfClass(DB.RevitLinkInstance).Where(lambda x: x.GetTypeId() == rvtLink.Id).First()

                #dtLinks.Rows.Add(rvtLink.Name, link.GetLinkDocument());





    # rlt = next((rlt for rlt in revit_link_types if rlt.LookupParameter("Type Name").AsString().rstrip(".rvt") == link_doc_title), None)
    # if rlt:
    # print "Updating workset visibility on this file: " + str(link_doc.Title)






 
    # # This finds the RevitLinkType element that matches the link_doc.
    # rlt = next((rlt for rlt in revit_link_types if rlt.LookupParameter("Type Name").AsString().rstrip(".rvt") == link_doc_title), None)
    # if not rlt:
        # #print "No matching RevitLinkType for the link_doc."
        # pass
    # else:
        # temp = "Updating workset visibility on this file: " + str(link_doc.Title)
        # print temp

        # # generate a list of the worksets in the link_doc
        # workset_table = link_doc.GetWorksetTable()
        # model_path = link_doc.GetWorksharingCentralModelPath()
        # lst_preview = WorksharingUtils.GetUserWorksetInfo(model_path)

        # # Populate list of worksets to enable
        # open_this_list_of_worksets = []
        
        # for objWorksetPreview in lst_preview:
            # wkset = workset_table.GetWorkset(objWorksetPreview.Id)
            
            # if hide_workset:
                # #gather a list of all the open worksets, EXCLUDING the worksets we want to hide
                # if wkset.IsOpen and not (wkset.Name == "Shared Levels and Grids" or wkset.Name == 'Match Lines' or wkset.Name == 'Other Model Content'):
                    # open_this_list_of_worksets.append(wkset.Id)
            # else:
                # #gather a list of all the open worksets, INCLUDING the ones we hid.
                # if wkset.IsOpen or wkset.Name == "Shared Levels and Grids" or wkset.Name == 'Match Lines' or wkset.Name == 'Other Model Content':
                    # open_this_list_of_worksets.append(wkset.Id)
        
        # # Set the WorksetConfiguration file to close all worksets, then open the ones from the list
        # workset_config = WorksetConfiguration(WorksetConfigurationOption.CloseAllWorksets)
        # workset_config.Open(open_this_list_of_worksets)
        
        # #reload the link with the updated workset configuration
        # rlt.LoadFrom(model_path, workset_config)
        
        # #delete the workset configuration after use
        # workset_config.Dispose()