Step 1: Creating your input files
=================================

Let's create Excel file examples. 


Requirements
^^^^^^^^^^^^

- A text editor or Excel

Overview
^^^^^^^^
You will need to supply the data and static images for the website. 
In addition, you will need a parameter file that specifies the figure parameters, text, and layout. 
The parameter file can be a regular text or Excel file. 

Fully working example input
^^^^^^^^^^^^^^^^^^^^^^^^^^^
An example is loaded with dataspectra in the folder sampleInput. 
To test dataspectra, you can use this and skip to Step 2. Or you can follow along with it as you
read below.

Input file organization
^^^^^^^^^^^^^^^^^^^^^^^

All the input, including data, images, and the parameter file 
should be in one folder. We will refer to this as the 
"input directory".

Input directory
    The folder or directory where all of your files are kept. 

Data files format
^^^^^^^^^^^^^^^^^

For the data file, your primary search term, should be on a column (rather than a row). 
This means that your data should usually be longer than wide. 

Parameter File format
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are 5 types of parameters to specify:

 - Dataset
 - Figure
 - Side Bar
 - Title Bar
 - Panel

Each type, except for title bar and side bar, can be used more than once.
You can use one parameter file that holds all of the parameters,
or you can separate the parameter file into individual files. 
Store all of these parameter files in one folder or directory. 

A template is included in excel, csv, and text format to build on.

Separate the columns with commas, tabs, or by Excel boxes.
Make sure to save the file with the appropriate suffix 
(.csv for commas-separated columns, .txt for tab-separated columns,
and .xlsx for Excel files) 

Note, if you are going to save  a comma-separated file, make sure to not include any commas within a particular text column. 

Unless otherwise specified, the variables for each parameter file should be
in the file format as (for e.g. in a csv file) ::
    variablename,Name of your variablename
    variablekey,Key of your variable

When specifying a new parameter type, you will need to specify the type in the first line. 

``parameter``
    Specify the type of parameter file. Options are { dataset, figure, panel, topbar }

::

    parameter,dataset


The Main Parameter Type
^^^^^^^^^^^^^^^^^^^^^^^

Description
+++++++++++

Here, you will specify and organize all of the parameter files you will be using. 




The Dataset parameter file
^^^^^^^^^^^^^^^^^^^^^^^^^^

Description
+++++++++++

You will need to create a separate dataset parameter file for each dataset. 
This file instructs how the dataset will be accessed and stored by the server. 
You can have multiple dataset parameter files. 

Variables
+++++++++

datasetkey
    A unique name you can specify to refer to this dataset in other files. 
datasetfile
    The actual name of this dataset file in the input directory. 
searchstart
    The row number (1-indexed) to start the search. 
searchcol
    The column number (1-indexed) where the primary key is held. 

Example  
+++++++ 

    datasetkey,braindata
    datasetfile,braindata.xlsx
    searchstart,2
    searchcol,1

The Figure parameter file
^^^^^^^^^^^^^^^^^^^^^^^^^

Description
+++++++++++

For each figure, you will need to create a separate figure parameter file. 
This file instructs how each figure accesses the data and how it is plotted. 
Because there a number of types of figures, we will only describe the format 
for 1 type - the boxplot. Check out the link for information on how to set 
up the other plots. 

Here, we will introduce the START term, which will be used in your figure 
parameter file to distinguish the variables from the ordered rows. 

To use this, the variables will go first, and then the START term,
and lastly the ordered rows. As the name suggests, the order of the ordered 
rows are important. 

Variables
+++++++++

``figurekey``
    A unique name for your figure

``figuretype``
    The type of figure. 
    Options are (boxplot, barplot, scatterplot, mdscatter, violin, carousel)

``valuelabel``
    The unit label for the value you want. This will usually be on the y-axis. 

``title``
    The name on the top of the figure. If you put "None" then no name will be placed.

``datasetkey``
    The datasetkey that this figure to accesses. 

Ordered rows (for boxplot)
++++++++++++++++++++++++++++

``BOX``, *name* , *colums* , *color*
    Adds a bar to your plot. *name* will be the label for this bar. 
    *columns* is a "$"-separated variable that refers to the columns 
    accessed in the data (e.g. 2$3$4 accesses columns 2-4 in the dataset). 
    *color* refers to the rgb values that are ";"-separated (e.g. 155;155;155).
``SPACE``
    Adds an empty space next to the bar. 

Example  
+++++++ 

::

    figurekey,myboxplot
    figuretype,boxplot
    valuelabel,FPKM
    title,Expression in brain
    datasetkey,braindata
    START
    BOX,Astrocytes,2$3$4,155;155;155
    BOX,Neurons,5$6$7,155;155;155
    BOX,Microglia,8$9$10,155;155;155
    SPACE
    BOX,Total,11$12$13,155;155;155


The Panel parameter file
^^^^^^^^^^^^^^^^^^^^

Description
+++++++++++

This file specifies the layout of the figure panels.
Here you can specify how the panels are laid out.  
the text in the tab info section, and the 

The section where the data is presented is the Panel section. So let's start there. 

An example file here perhaps ::

    panelkey,brain
    citetext,The brain expression project. John Doe et al. 
    citelink,www.dataspectra.organization
    infotitle,Cell type specific expression in brain. 
    infotext,Brain expression. 
    start
    FIGURE,myboxplot,100,300,1,1
    FIGURE,mybarplot,50,300,2,1
    FIGURE,anotherbarplot,50,300,2,2

Variables
+++++++++

panelkey: Each panel has a 

start: This specifies that below this we are going to list the organization of the figures. 
BREAK - indicates
SPACE


The Side Bar parameter file
^^^^^^^^^^^^^^^^^^^^^^^^^^^

default searchTerm
defaultbutton 



Description
+++++++++++

This file allows you to specify how the side bar is laid out. 

Variables
+++++++++


The Title Bar parameter file
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Description
+++++++++++


Variables
+++++++++


FAQ
^^^



Troubleshooting
^^^^^^^^^^^^^^^

- All of the files should be in one folder. 
- Files can be either .csv, .txt, or .xlsx. 
- .txt files should be Tab-delimited. 
- If you are using Excel, only the first sheet of each .xlsx file will be used. 
