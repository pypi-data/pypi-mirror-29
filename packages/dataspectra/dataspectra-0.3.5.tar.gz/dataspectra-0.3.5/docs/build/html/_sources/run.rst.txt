Step 3: Running Dataspectra
===========================

Overview
^^^^^^^^

This will require 3 minutes of work. But there is a waiting step. 

This is the final step for getting your Dataspectra site up and running. 
It will take your parameter file and dataset, and create files so 
that Google App Engine will know how to render your website. 
It will also upload your data to the Google Cloud Platform.

Requirements
^^^^^^^^^^^^

 * Python 2.7 (should already be installed on a Mac).


Make sure prior steps are completed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You should have the following:

#. An folder that has both your parameter file and your datasets. These should be in the **same** folder. 
#. A projectID from setting up your Google Cloud Platform account
#. A .json file in your google-cloud-sdk folder from authentication. 

If any of these are missing, then go back to the previous steps to complete. 


Install Dataspectra
^^^^^^^^^^^^^^^^^^^

#. Open your Terminal.  (Found in Finder -> Application -> Utilities)
#. Type in :
   ::

        sudo easy_install pip
#. Press Return
#. Type in: 
   ::

        pip install dataspectra

Run Dataspectra
^^^^^^^^^^^^^^^

#. Open your Terminal. 
#. Type in the following - while replacing the [TERM]s (see below): 
   ::

        dataspectra fulldeploy -i [PARAMETERFILE] -c [AUTHENTICATIONFILE] -p [PROJECTID]
#. Press Return and wait. 

The [XX-FILE]s can be filled in by dragging and dropping the file 
onto the terminal window while typing in the command. Alternatively, 
you can just manually type in the full path.  

The [PARAMETERFILE] is the parameter file within the input folder. 
The [AUTHENTICATIONFILE] is the .json file that was downloaded in the prior step. 

The [PROJECTID] is the project ID. 

This command may look like this:

::

    dataspectra fulldeploy -i /Users/ryosukekita/Desktop/dataspectra_input/dataspectra.tutorial.parameters.xlsx
    -c /Users/ryosukekita/Desktop/google-cloud-sdk/brainspandemo-615065a965401.json -p brainspandemo

Notes:
- Make sure your computer is hooked up to the internet while this 
is happening. You may have to turn the sleep function off of your
computer if you'll be leaving your computer unattended. 

Check out your new website!
^^^^^^^^^^^^^^^^^^^^^^^^^^^

After Dataspectra is complete, open up your browser 
and go to [PROJECTID].appspot.com
[PROJECTID] should be your project ID. 







