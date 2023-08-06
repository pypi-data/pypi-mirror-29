Overview
^^^^^^^^

Why use Dataspectra?
====================

Traditionally, creating an interactive data visualization 
on the web required multiple time-consuming steps.

1. Your data 
2. A design of how the web page looks. 
3. Uploading your data to a web server. 
4. Code to access your data. 
5. Code to plot the data. 
6. Code to arrange the plots, text, and web design. 
7. Access to a web-server that will handle the user-interactions. 

Dataspectra makes this process easier by doing all of the
coding and uploading processes for you. So now, all you 
need to do are the following:

1. Your data 
2. An excel file describing how you want your page/figures to look.
3. Dataspectra

You can think of it like the Squarespace for web-visualization of data.  

There are a lot of tools out there for doing similar things. 
These include Plotly Dash or R Shiny. Dataspectra fits the niche
of projects where you want a free-standing website, that is low-cost and
low-setup time. Also it works wonderfully with large datasets. 

How does Dataspectra work?
==========================

To create a dataspectra page, there are three main parts. 

Step 1: Gather your data and design your web page. 

Step 2: Create a Google Cloud Platform account. 

Step 3: Run Dataspectra. 

The application will upload your data in Step 1 to the Google Cloud Datastore. 
Dataspectra will also convert your website design parameters in Step 1
to a readable format for the Google App Engine. Then, whenever a user searches for a particular
term, the term will be queried in the Google Cloud Datastore, and the figure will be rendered
as specified.  

When should I use Dataspectra?
==============================

The main use scenario for dataspectra is when you have the following:

#. A dataset with a lot of rows.
#. The rows have a primary search term. 
#. A need for a quick and easy way to view a figure for any particular row.

For example, this type of data is common in genomics, where people are interested in seeing the data for a particular gene. With over 20,000 genes in the human genome,
it is impossible to plot all of the data in one figure. So a Dataspectra site can help users search the data for their favorite gene quickly and easily. 
You can imagine that this scenario would also be encountered in other type of data, for example a long list of dates or a long list of geographic locations. 


About the documentation
=======================

Steps 1, 2, and 3 will demonstrate how dataspectra works in a tutorial format. 

To simply test whether dataspectra works, you can download the tutorial files in Step 1, 
and continue onto Steps 2 and 3. This will eliminate the most time consuming step (Step 1). 

"Parameters" describes the full set of available parameters for customization. 

"Advanced" describes how to perform more advanced functions like setting up passwords, 
adding your own domain, accessing meta files, or fixing aspect ratios.  

"Examples" describes more figure types that can be created. 

