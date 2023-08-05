Piccolo5/Piccolo6/Picalor6 Python API calling interface

What is it?
-----------
A python package enabling users to call a set of Picwin32.dll or Ganessa_SIM.dll API functions and subroutines within python scripts. 

Installation
------------
:Windows only: 

	pip install ganessa

Requirements
------------

  #) python requirements: numpy 1.7 or above
  #) Piccolo or Picalor kernel library (picwin32.dll), starting from version 5 (141203)
  #) valid Piccolo or Picalor license

This tool requires Picwin32.dll to be in the PATH or in one of the following folders:
 [ C: or D: ] / ['Program Files/Adelior/Piccolo5_' or 
				 'Program Files (x86)/Gfi Progiciels/Piccolo6_'  or
				 'Program Files (x86)/Gfi Progiciels/Picalor6_']
				 'Program Files (x86)/Safege/Ganessa_']
			  + ['fr' or 'uk' or 'esp' or 'eng']

    Or one of Ganessa_SIM.dll or Ganessa_TH.dll in:
 [ C: or D: ] / ['Program Files (x86)/Safege/Ganessa_']
			  + ['fr' or 'uk' or 'esp' or 'eng']

Content
-------

The package provides:
 #) 'sim' package:
     - a few basic functions for reading or loading a model, running simulations
     - 'getter' functions for individual objects and attributes, time series vectors, attribute vector of all object
     - iterators over links, nodes, tanks, demands, and tables, or over Piccolo selections
 #) 'th' package: same functions except running extended period simulations and time series getters
 #) 'util' package: miscellaneous functions
 #) 'OpenFileMMI' provides classes for opening dialog frame for a .dat/.bin model file, and output (result) file
 #) 'sort' provides a heapsort based on heapq
 #) 'midfile' provides minimal mif/mid functions similar to shp/dbf shapefile  handler (pyshp package)
 #) 'epanet' provides epanet2 python API (thanks to Assela Pathirana - mailto: assela@pathirana.net) for win32 
    similar to EpanetTools-0.4.0
 #) 'parallel' provides a simple parallel simulations handling framework based on multiprocessing.

Model object and parameters can be modified using Piccolo command language (see cmd, cmdfile and execute)
A documentation is provided as pyGanessa.html in the intallation folder.

History of the document
-----------------------
Created 2013-07-04
Revised 2015-05-03: since 2014-12-04 Picwin32.dll is compatible with this API
Revised 2016-07-07: provided as .rst
Revised 2017-08-08: install using pip; Piccolo/Ganessa dll folder search order.
Revised 2017-09-12: split sim into core, core_sim, core_th
Revised 2017-11-13: added sort, midfile, epanet modules
Revised 2017-11-30: added parallel


