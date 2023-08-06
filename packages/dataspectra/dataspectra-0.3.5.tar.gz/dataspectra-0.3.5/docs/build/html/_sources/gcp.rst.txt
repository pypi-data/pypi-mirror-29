Step 2: Setting up Google Cloud Platform
========================================

Overview
^^^^^^^^

This will take 7-10 minutes of work.

Google Cloud Platform is a service that hosts your data 
and web page.
This allows anyone with the link to access your webpage. 
In this section, we will setup your Google Cloud Platform account
and hook it up to the computer you will use to run Dataspectra. 

The steps described here is the standard approach for 
the setting up the Google Cloud Platform. If you would like
to use their documentation, 
I have included the relevant links at the bottom. 

First, create a Google Cloud Platform account
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Login to your regular Google account. 
#. Go to: https://cloud.google.com/
#. Click CONSOLE in the upper right corner
#. Agree to the Terms of Service
#. Click "Select a project" (at the top). 
#. Click on the "+" sign at the top right. 
#. Provide a unique name. Write down the ProjectID that is given to you. (Tip: if your unique name is long and unique enough, your ProjectID will be the same as your unique name). 
#. Click Create. 
#. Wait until your project activates (watch the spinning circle at the top right). 

Next, activate Google Cloud Datastore
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Datastore will hold your dataset for you on the web. 
This will allow for quick queries to specific rows in your dataset

#. Make sure you're at the Google Cloud Console (console.cloud.google.com)
#. Click on "Select a Project" and select the project that you just created. 
#. On the left side bar, scroll down to "Datastore" and click it. 
#. Click on Create Entity, and select the region closest to you. 
#. Click next, and wait while the datastore is activating.
#. Once activated, you don't actually need to create an entity. 

Next, activate Google Cloud Billing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Although Dataspectra is free, there **may** be cost to hosting 
on Google Cloud Platform. I say "may" because Google Cloud
has a fantastic free tier, so sites that aren't that frequently
accessed (like most small scale Dataspectra sites), should be free.
However, because there is a possibility of a cost, we must activate
billing for things to work. But we can set a budget limit so that you
don't incur unexpected costs. 

#. Make sure you're at the Google Cloud Console. 
#. Go to the menu at the top left. Scroll down and click billing. 
#. Click link a billing account, and then create a billing account. 
#. Fill out the billing information, and it'll take you back to the overview. 
#. Click on "Budgets and Alerts" on the left sidebar. 
#. Click "Create a budget".
#. Put in a budget name (anything is fine). 
#. Add your spending limit. I usually put $10. 
#. Then save your settings.  


Then, install the Google Cloud Software Development Kit (SDK)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Google Cloud SDK will be installed on the computer that 
you will run Dataspectra on. The SDK will allow your computer
to send the data and rendered website information to the Google
Cloud Server. 

#. Download the google-cloud-SDK from the following link: https://cloud.google.com/sdk/docs/
#. Extract the downloaded file by double clicking the downloaded *.tar.gz file. 
#. Move the google-cloud-sdk folder to your Desktop. 
#. Open Terminal, found in Finder --> Applications --> Utilities
#. Then, open up the google-cloud-sdk folder and drag and drop the install.sh file to the Terminal window. 
#. Press Return, and continue to press Return until the command line reappears again.

Finally, set up authentication for the Google App Engine
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Go back to your Gogle Cloud Console (console.cloud.google.com)
#. Make sure your project is selected at the top (Click "Select a project", if necessary)
#. Click on the Menu at the top left. 
#. Go to APIs & Services and click on credentials (may be the Key icon). 
#. Click on the "Create service account key"
#. Under service account, choose App Engine default service account. 
#. Click Create. 
#. A file will be downloaded. 
#. Take downloaded file and move it to the google-cloud-sdk folder in your desktop from the above step.  
#. Go back to your Terminal, (found in Finder --> Applications --> Utilities)
#. Type in:
   ::

        gcloud auth login
#. Press Return 

Relevant Google Cloud Platform links
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The above is a streamlined process for
the standard way of setting up Google App Engine. 
You can see their full documentation here. 

Google App Engine Setup: 
https://cloud.google.com/appengine/docs/standard/python/quickstart

Installing Google Cloud SDK:
https://cloud.google.com/appengine/docs/standard/python/download

Authenticating Google Cloud Datastore API:
https://cloud.google.com/datastore/docs/reference/libraries#client-libraries-install-python
https://cloud.google.com/docs/authentication/getting-started
