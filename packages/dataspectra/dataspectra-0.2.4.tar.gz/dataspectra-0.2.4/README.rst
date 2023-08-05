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

Installing Google Cloud SDK For Python
======================================
Step 1: Download the google-cloud-SDK
https://cloud.google.com/sdk/docs/
Step 2: Extract the package by double clicking the *.tar.gz file. 
Step 3: Move the folder to your Desktop
Step 4: Type ~/Desktop/google-cloud-sdk/install.sh
- Keep on pressing enter. 

Step 5: Click on Datastore. 
- Activating datastore. 
- Click on Create an Entity. 
- Your first entity
- Choose the region where it is most likely to be. 
- Wait. 

Click on AppEngine

Activating budget. 


Step 5: Authenticating: 
https://cloud.google.com/docs/authentication/getting-started
Go to console.cloud.google.com
Click on the Menu at the top left. 
Go to APIs & Services
Click on the Key in the left side bar. 
Click on the "create service account key"
Put any name down.  
- Then specify Role Owner
Click on create.
Move the file to your google-cloud-sdk folder. 
Type in export GOOGLE_APPLICATION_CREDENTIALS="/..

#Authenticate your login
gcloud auth login

Step 2: Install using: gcloud components install app-engine-python
