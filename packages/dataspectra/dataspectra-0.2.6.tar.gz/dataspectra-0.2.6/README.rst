Dataspectra
^^^^^^^^^^^

A python package to create interactive web visualizations. 


Requirements:
=============
- Python2.7


Installation
=============
.. code-block:: bash
    
    $ pip install virtualenv
    $ virtualenv ~/virtualenv/ds
    $ source ~/virtualenv/ds/activate
    $ pip install dataspectra


Running
=======
.. code-block:: bash

    $ source ~/virtualenv/ds/activate
    $ dataspectra


Authenticating
==============
- Need to allow for google cloud datastore authentication

Development of the web/app_engine
=================================
- In order to test new functions you will need Google Cloud SDK
- Test using dev_appserver.py --clear_datastore=yes app.yaml in the sample output. 
- Once your code looks good. You can copy it to the source code in aefiles. 

Development For Ryo
====================
- Problem with rapid updates, since you will have to continually copy files back and forth to the source directory. 
- To fix this - you can create a symbolic link from the source directory to your output directory.
- Go to the symbolic link, and run dev_appserver.py 
- Then you can quickly

dataspectra develop - will create new output files - and then copy those files to the original aefiles directory. 


- For updating the documentation. 
  Make sure you're in virtualenv ds or dstest. 
  command-shift-R for preview. 

- For developing the package
  python setup.py develop

   For uploading to pypi
   python setup.py sdist upload

   

