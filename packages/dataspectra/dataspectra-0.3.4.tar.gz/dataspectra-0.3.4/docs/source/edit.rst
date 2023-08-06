Editing an existing page
^^^^^^^^^^^^^^^^^^^^^^^^


There are three ways to edit your page after you 
deploy it the first time. 

Reupload everything
===================

Do this if you want the easiest way (at the potential cost of
more waiting time). 
You can simply edit your parameter files and your data
within your input folder. 
Just run the same command:

::

    dataspectra fulldeploy -i [PARAMFILE] -c [AUTHFILE] -p [PROJECTID]


Reupload only the parameter file
================================

If you only changed the parameter file, and you're not adding 
any new datasets, you can run the command:

:: 

    dataspectra deploy -i [PARAMFILE] -c [AUTHFILE] -p [PROJECTID]


Reupload only the datasets
==========================

If you updated the dataset, but not the paramter file, you can
run the command:

::

    dataspectra upload -i [PARAMFILE] -c [AUTHFILE] -p [PROJECTID]




