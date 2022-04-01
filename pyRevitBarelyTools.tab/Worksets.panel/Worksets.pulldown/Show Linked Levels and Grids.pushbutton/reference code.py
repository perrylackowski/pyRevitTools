# """
# HIDE / UNHIDE - LEVELS AND GRIDS FROM LINKS DOCUMENTS

# TESTED REVIT API: 2017, 2018

# Author: min.naung@https://twentytwo.space/contact | https://github.com/mgjean

# This file is shared on www.revitapidocs.com
# For more information visit http://github.com/gtalarico/revitapidocs
# License: http://github.com/gtalarico/revitapidocs/blob/master/LICENSE.md
# """

# import System
# from System.Collections.Generic import List
# from Autodesk.Revit.DB import Transaction
# from Autodesk.Revit.DB import *

# doc = __revit__.ActiveUIDocument.Document
# active_view = doc.ActiveView

# # filter name "can name anything"
# ifilter = "GiveFilterAName"

# endWiths = "Anything"

# # filter check
# found = False

# unhide = False # Edit here to hide/unhide
# msg = "Unhide" if unhide else "Hide"
# trans = Transaction(doc,"%s links levels grids" %(msg))
# trans.Start()

# # collect all filter elements
# allFilters = FilteredElementCollector(doc).OfClass(FilterElement).ToElements()

# # get filters from current view
# viewFilters = active_view.GetFilters()
# # collect filters' names
# viewFiltersName = [doc.GetElement(i).Name.ToString() for i in viewFilters]

# # loop each filter
# for fter in allFilters:
	# # filter already have in doc but not in current view
	# if ifilter == fter.Name.ToString() and ifilter not in viewFiltersName:
		# # add filter
		# active_view.AddFilter(fter.Id)
		# # set filter visibility
		# active_view.SetFilterVisibility(fter.Id, unhide)
		# found = True
	# # filter already have in doc and current view
	# if ifilter == fter.Name.ToString() and ifilter in viewFiltersName:
		# # set filter visibility
		# active_view.SetFilterVisibility(fter.Id, unhide)
		# found = True
		
# # if filter not found in doc
# if not found:
	# # all grids in doc
	# grids = FilteredElementCollector(doc).OfClass(Grid).ToElements()
	# # all levels in doc
	# levels = FilteredElementCollector(doc).OfClass(Level).ToElements()
	# # collect category id from grid and level
	# CateIds = List[ElementId]([grids[0].Category.Id,levels[0].Category.Id])
	
	# # type ids from grids 
	# gridTypeIds = set([i.GetTypeId() for i in grids])
	# # type ids from levels
	# levelTypeIds = set([i.GetTypeId() for i in levels])
	
	# # get grid type element
	# type_elems = [doc.GetElement(i) for i in gridTypeIds]
	# # get level type element
	# type_elems.extend([doc.GetElement(l) for l in levelTypeIds])
	
	# # loop type elements
	# for elem in type_elems:
		# # if endwiths not include in type name
		# if not endWiths in elem.LookupParameter("Type Name").AsString():
			# # add endwiths in type name
			# elem.Name = elem.LookupParameter("Type Name").AsString() + endWiths
	# # get type names
	# type_names = [i.LookupParameter("Type Name").AsString() for i in type_elems]
	# # type name parameter id
	# paramId = type_elems[0].LookupParameter("Type Name").Id
	# # create a "not ends with" filter rule
	# notendswith = ParameterFilterRuleFactory.CreateNotEndsWithRule(paramId,endWiths,False)
    # elem_filter = []
    # elem_filter.Add(notendswith)
	# # create parameter filter element
	# paramFilterElem = ParameterFilterElement.Create(doc, ifilter,CateIds,elem_filter)
	# # set filter overrides (same with add filter to current)
	# active_view.SetFilterOverrides(paramFilterElem.Id, OverrideGraphicSettings())
	# # set filter visibility
	# active_view.SetFilterVisibility(paramFilterElem.Id, unhide)
	
# print "DONE!"
# trans.Commit()

'''
HIDE - LEVELS AND GRIDS FROM LINKS DOCUMENTS
'''
from pyrevit import DB
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.DB import WorksharingUtils
from Autodesk.Revit.DB import WorksetConfiguration
from Autodesk.Revit.DB import RevitLinkType
from Autodesk.Revit.UI import TaskDialog

from pyrevit import script
output = script.get_output()

import traceback

doc = __revit__.ActiveUIDocument.Document
app = __revit__.ActiveUIDocument.Application.Application

for link_doc in app.Documents:
    print link_doc.Title

print "Titles for each Document in app.Documents \n\n "
for link_doc in app.Documents:
    
    print link_doc.Title
    
    #this excludes the project file itself
    if not link_doc.IsLinked:
        print "this one isn't linked \n\n "
        continue
        
    #This gets a list of the RevitLinkTypes in the active document.
    revit_link_types = FilteredElementCollector(doc).OfClass(DB.RevitLinkType).ToElements()
    
    #link_doc_title = link_doc.Title
    #e = next((e for e in revit_link_types if e.LookupParameter("Type Name").AsString().rstrip(".rvt") == link_doc_title), null)
    #if e:
        #do stuff
    #else:
        #print "e equals null?"
        
    for e in revit_link_types:
        
        #This finds the revitLinkType element (the revit project links) that matches the link_doc.
        try:
            #print e.Name #this fails in python due to python's multiple class inheritance: https://github.com/DynamoDS/DynamoRevit/issues/1881
            #so use this instead. it grabs the parameter for the type name, converts to a string, then removes the ".rvt" so it can be compared to the Title
            a = e.LookupParameter("Type Name").AsString().rstrip(".rvt")
            b = link_doc.Title
            if a == b:
                temp = "WE HAVE A MATCH:" + str(type(e)) + output.linkify(e.Id)  
                print temp
                
                
                temp = "perform an operation on this file: " + str(link_doc.Title) + ", "+ e.LookupParameter("Type Name").AsString().rstrip(".rvt")
                print temp
                

                # generate a list of the worksets in the link_doc
                workset_table = link_doc.GetWorksetTable()
                model_path = link_doc.GetWorksharingCentralModelPath()
                lst_preview = WorksharingUtils.GetUserWorksetInfo(model_path)

                close_this_list_of_worksets = []
                
                for objWorksetPreview in lst_preview:
                    wkset = workset_table.GetWorkset(objWorksetPreview.Id)
                    
                    temp = wkset.Name + " is open: " + str(wkset.IsOpen)
                    print temp
                    
                    if not wkset.IsOpen:
                        close_this_list_of_worksets.append(wkset.Id)
                    
                    if wkset.Name == "Shared Levels and Grids":
                        print "found it. close this one."
                        close_this_list_of_worksets.append(wkset.Id)
                    
                print "closing these worksets:"
                for workset in close_this_list_of_worksets:
                    print workset
                
                workset_config = WorksetConfiguration()
                workset_config.Close(close_this_list_of_worksets)

                
                #apparently this doesn't work for reloading worksets like it's supposed to...
                #e.LoadFrom(link_doc.GetWorksharingCentralModelPath(), workset_config)
                
                
                
                
                # # # foreach (var key in result.Keys)
                # # # {
                    # # # var linkpath = key;
                    # # # var openids = result[key].OpenedList.Select(x => x.Id).ToList();
                    # # # var closeids = result[key].ClosedList.Select(x => x.Id).ToList();

                    # # # var config = new WorksetConfiguration(WorksetConfigurationOption.CloseAllWorksets);
                    # # # if (openids != null && openids.Any())
                    # # # {
                          # # # config.Open(openids);
                    # # # }

                    # # # filePath = new FileInfo(linkpath);
                    # # # mp = ModelPathUtils.ConvertUserVisiblePathToModelPath(filePath.ToString());
                    # # # linktitle = Path.GetFileName(linkpath);
                    # # # rlt = rvtlinktypes.FirstOrDefault(x => x.Name.Equals(linktitle)) as RevitLinkType;

                    # # # doc.Delete(rlt.Id);
                    # # # doc.Regenerate();
                    # # # RevitLinkOptions option = new RevitLinkOptions(true);
                    # # # option.SetWorksetConfiguration(config);
                    # # # RevitLinkType.Create(doc, mp, option);
                # # #}
                
                
                print "starting transaction"
                t = Transaction(doc)
                t.Start('close open worksets?')                
                
                #chuck = next((e for e in employees if e.name == "Chuck"), None)
                #print(chuck.name)
                
                doc.Delete(e.Id)
                
                doc.Regenerate()
                
                #create a model path to pass to the revitLinkType.Create function
                path_name = link_doc.PathName
                mp = ModelPathUtils.ConvertUserVisiblePathToModelPath(path_name)
                
                #create an instance of the RevitLinkOptions class that contains the desired workset configuration
                option = RevitLinkOptions(True)
                option.SetWorksetConfiguration(workset_config)
                
                RevitLinkType.Create(doc, mp, option)
                
                t.Commit()
                print "done reloading"
                
                workset_config.Dispose()
                print "done disposing"
                break


        
        except Exception as mesg:
            print "\n\n exception :("
            print mesg
            print(traceback.format_exc())
            print "exception :("
            

    print "\r\n\r\n"
    




    
    
    
    
    

# #gets all rvt links that are LOADED. Also includes the project itself
# for linkdoc in app.Documents:

    # print "\r\n" + str(linkdoc.Title)
    
    # #this excludes the project file itself
    # if not linkdoc.IsLinked:
        # print "this one isn't linked"
        # continue
        
    # workset_table = linkdoc.GetWorksetTable()
    # lstPreview = WorksharingUtils.GetUserWorksetInfo(linkdoc.GetWorksharingCentralModelPath())
    
    # for item in lstPreview:
        # workset_configurationset = workset_table.GetWorkset(item.Id)
        # if workset_configurationset.Name == "Shared Levels and Grids":
            # print "found it!"
        # if (workset_configurationset.IsOpen):
            # print str(workset_configurationset.Name) + ": Open" + "\r\n"
        # else:
            # print str(workset_configurationset.Name) + ": Closed" + "\r\n"
# #TaskDialog.Show("Info", info)







# try:
    # RvtLinkType_elem_lst = FilteredElementCollector(doc).OfClass(DB.RevitLinkType).ToList()

    # for _linkdoc in app.Documents:
        # if not _linkdoc.IsLinked:
            # continue
        # RevitLinkType _RvtLinkType = null

        # for elmnt in RvtLinkType_elem_lst:
            # _RvtLinkType = elmnt as RevitLinkType
            # if _RvtLinkType.Name is not _linkdoc.Title:
                # continue
            # else:
                # break

        # lstworkset_configurationSetIds_Close = []
        # #lstworkset_configurationSetIds_Open = []
        # #lstworkset_configurationSetIds_Open = new List<WorksetId>();

        # workset_configuration = WorksetConfiguration()
        # ModelPath _modelpath = _linkdoc.GetWorksharingCentralModelPath()
        # WorksetTable _worksetTable = _linkdoc.GetWorksetTable()
        # IList<WorksetPreview> lstPreview = WorksharingUtils.GetUserWorksetInfo(_modelpath)

        # for item in lstPreview:
            # workset_configurationset = _worksetTable.GetWorkset(item.Id)
            
            # if not workset_configurationset.IsOpen:
                # lstworkset_configurationSetIds_Close.Add(workset_configurationset.Id)
                # continue

            # # // Or :
            # # //if (workset_configurationset.IsOpen)
            # # //{
            # # //    lstworkset_configurationSetIds_Open.Add(workset_configurationset.Id);
            # # //    continue;
            # # //}
            
        # workset_configuration.Open(lstworkset_configurationSetIds_Close)
        
        # # //or
        # # //workset_configuration.Close(lstworkset_configurationSetIds_Open);
        
        # _RvtLinkType.LoadFrom(_modelpath, workset_configuration);
# except e:
    # print e.Message
    # print "failed"
# print "succeeded"
       
    


















