
'''
Script to plot summary snowpit from data example of the standard snowpit format
Simon Filhol, December 2016

'''

from snowpyt import pit_class as pc

filename = '/home/tintino/github/snowpyt/snowpyt/data_example/20170209_Finse_snowpit_reverseY.xlsx'  #[insert path to file]

pit1 = pc.Snowpit()
pit1.filename = filename
pit1.import_xlsx()
pit1.plot(metadata=True)
pit1.plot(plots_order=['density', 'temperature', 'stratigraphy','crystal size', 'sample value'])

pit1.plot(plots_order=['density', 'sample names','sample values'])



#================================================================================
#       Import CAAML snowpit format
#================================================================================
import pit_class as pc
f = '/home/tintino/Documents/snowschool_lautaret_2018/all_data/20180214_snowpit_openfield_4.caaml'
f='/home/tintino/Documents/snowschool_lautaret_2018/all_data/201802141205_PitForest.caaml'
f = '/home/tintino/Documents/snowschool_lautaret_2018/201802161132.SimpleProfile-1.caaml'
p = pc.Snowpit()
p.filename=f
p.import_caamlv6()
p.plot(plots_order=['density', 'temperature', 'stratigraphy'], metadata=True)
p.plot(plots_order=['density', 'temperature', 'stratigraphy', 'hardness'])


#================================================================================
#       Section for Debugging the package
#================================================================================
# Code to run my local version of the package the local
import sys
sys.path.append('/home/tintino/github/snowpyt/snowpyt/')
import pit_class as pc

p=pc.Snowpit()
p.filename='/home/tintino/github/snowpyt/snowpyt/data_example/20170209_Finse_snowpit.xlsx'  #[insert path to file]
p.import_xlsx()
p.plot(plots_order=['density', 'sample names','sample values'])

#