'''
Goes to Manage > Manage Links > Manage Worksets and opens these worksets for each LOADED link:

["Shared Levels and Grids", "Match Lines", "Other Model Content"]

TESTED REVIT API: 2020

Author: Robert Perry Lackowski

'''

import workset_functions

#list the Worksets you want to update. True indicates Show, False indicates Hide
workset_functions.update_worksets(["Shared Levels and Grids", "Match Lines", "Other Model Content"], True)

print "\n Script complete."