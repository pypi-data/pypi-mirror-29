Step 1: Creating your input files
=================================


Requirements
^^^^^^^^^^^^

- A text editor or Excel

Overview
^^^^^^^^
To create your website, you will need to supply the data
that your website uses.
In addition, you will need a parameter file that specifies
how the webpage will look.
The parameter file can be a regular text or Excel file. 
Here, we will talk about what format your data files should be
and how to create your parameter file. 


Tutorial
^^^^^^^^

To download the helper files, you can click `here <www.dataspectra.org>`_.

In the downloaded folder, you will find example_files and tutorial_files. 
The tutorial_files contains the tutorial data file and a complete tutorial parameter file.
To simply test dataspectra, you can use these and skip to Step 2. 
You can also follow along with it as you read the documentation below.

tutorial_files
    The input directory where the example files are located.
ds.tutorial.data.csv
    The example tutorial dataset file. 
    The primary search term is in the first column.
    The rest of columns are different samples. 
    The rows represent different genes. 
ds.tutorial.metadata.csv
    A file that holds the metadata for the data file. 
ds.tutorial.parameters.xlsx
    The example tutorial parameter file. Information about 
    this file is described below. 
ds.parameter.template.xlsx
    The file has the template for a parameter file, 
    with no information filled in.
  

Organization of Input Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^

All the input, including the data file and the parameter file 
should be in one folder. We will refer to this as the 
"input directory".

Input directory
    The folder or directory where all of your input 
    files are kept. 

Data Files Overview
^^^^^^^^^^^^^^^^^^^

The data files are the large tables that hold the data that you would like to plot. 
Your primary search terms should be along one column (rather than a row). 
This means that your data should usually be taller than wide. 

Primary search terms
    The terms that your user will search for in your website.

Parameter Files Overview
^^^^^^^^^^^^^^^^^^^^^^^^

The parameter file specifies how your webpage looks and 
how your data file is formatted.

.. image:: layout_parameters.png

There are 5 types of parameters to specify:

 - Figure
 - Side Bar
 - Site
 - Panel
 - Dataset

Each type, except for the "Site" and "Side Bar", can be used more than once.
For example, you may have multiple datasets or multiple figures.
In addition to the tutorial file that has a completed working parameter file, 
a template parameter file is included (ds.parameter.template.xlsx)
 to guide you in creating your own parameter file.

The columns should be separated by Excel boxes, commas, or tabs depending
on the type of file you're saving it as. Make sure to save the file with the appropriate suffix 
(.csv for commas-separated columns, .txt for tab-separated columns,
and .xlsx for Excel files) 

Note, if you are going to save a comma-separated file,
make sure to not include any commas within a particular 
text column. 

Unless otherwise specified, the variables for each parameter file should be
in the file format as (for e.g. in a csv file) ::
    variablename,The name of your variable
    variablekey,The variable key that you want to use

When specifying a new parameter type (e.g. a new figure, dataset, or panel)
, you will need to specify the type in the first line of the parameter. 

``parameter``, *parameterType*
    Specify the type of parameter file. Options are { dataset, figure, panel, site, sidebar }

::

    parameter,dataset


The Site Parameter Type
^^^^^^^^^^^^^^^^^^^^^^^

Description
+++++++++++

With the site parameter, you will specify the parameters for the entire site. 

Variables
+++++++++

``sitename``, *name*
    The main title name for you website
``topname``, *name*
    A subheader name for your website. 
    This is often your name or your lab name.
``toplink``, *websiteLink*
    A website link for that redirects when 
    topname is clicked. This is often your personal web page
    or you lab web page. 
``defaultterm``, *defaultTermName*
    The default search term that is initially used 
    when visiting the site. 
``theme``, *themeName*
    The style of your website. Options are "light" or "dark"
``defaultpanel``, *defaultPanelName
    The default panel that is initially displayed. 

Example Site Parameter
++++++++++++++++++++++

::

    parameter,site
    sitename,BRAINSPAN
    topname,DATASPECTRA
    toplink,www.dataspectra.org
    defaultterm,ARX
    theme,light
    defaultpanel,agepanel




The Dataset Parameter Type
^^^^^^^^^^^^^^^^^^^^^^^^^^

Description
+++++++++++

With the dataset parameter, you will specify how the data will be accessed and stored by the server. 
You can have multiple dataset parameter files. 

Variables
+++++++++

``datasetkey``, *name*
    A unique name you will use to refer to this dataset in other parameters. 
``datasetfile``, *filePath*
    The actual name of this data file in the input directory. 
``searchrowstart``, *number* 
    The row number (one-indexed) to start the search. 
``searchcol``, *number*
    The column number (one-indexed) where the primary search term is located. 

Example  
+++++++ 
::

    parameter,dataset
    datasetkey,brainspandata
    datasetfile,ds.tutorial.data.xlsx
    searchcol,1
    searchrowstart,2



The Side Bar Parameter Type
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Description
+++++++++++

With the sidebar parameter, you will specify how the side bar is displayed. 
Because the order of the sidebar elements matter, you will start off 
by using the "START" term. This indicates that the following elements
are ordered. 


Ordered Variables
+++++++++++++++++

``START``
    Specifies that the subsequent terms should be ordered in the corresponding manner. 
``SEARCH``, *placeholder*
    Creates the search box. *placeholder* is placed as the placeholder text in the search box.  
``SPACE``
    Creates a space in the side bar. 
``BUTTON``, *buttonText*, *panelkey*
    Creates a button that links to a specific panel.
    The text inside the button is specified by *buttonText*. 
    The panel that it will link to is specified by *panelkey*.

Example
+++++++

::

    START		
    SEARCH,SEARCH	
    SPACE		
    BUTTON,Age,agepanel
    BUTTON,Distributions,distributionpanel


The Figure parameter file
^^^^^^^^^^^^^^^^^^^^^^^^^

Description
+++++++++++

The figure parameter file encompasses all objects 
in the panel. This includes plots and titles. 
For each figure, you will need to create a separate 
figure parameter file. This file instructs how each 
figure accesses the data and how it is plotted. 
Because there a number of types of figures, we will 
only describe the format for 2 type - the title figure,
and the boxplot. Check out "Parameters" link for more
detail on the other plots.

Here, we also have the START term, which will be used 
in your figure parameter file to distinguish the 
variables from the ordered rows. 

The unordered variables will go first, 
and then the START term, and lastly the ordered rows. 
As the name suggests, the order of the ordered 
rows will be implemented in the panel.

Unordered Variables
+++++++++++++++++++

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
``xtickfontsize``
    This (when relevent) specifies the font size (in px) of your x-axis. 
``xtickangle``
    This (when relevent) specifies the angle of orientation of your tick labels. 
    (0 is horizontal, 90 is vertical)

Ordered varaibles (for barplot)
++++++++++++++++++++++++++++++

``START``
    Specifies that the subsequent terms 
    should be ordered in the corresponding manner. 
``BAR``, *name* , *colums* , *datatype*, *color*
    Adds a bar to your plot. *name* will be the label for this bar. 
    *columns* is a "$"-separated variable that refers to the columns 
    accessed in the data (e.g. 2$3$4 accesses columns 2-4 in the dataset). 
    *color* refers to the rgb values that are ";"-separated (e.g. 155;155;155).
    *datatype* should be "data", unless using an advanced function for specifying columns.
    See the Advanced section for more detail. 
``SPACE``
    Adds an empty space next to the bar. 

Ordered variables (for title)
++++++++++++++++++++++++++++++

``START``
    Specifies that the subsequent terms 
    should be ordered in the corresponding manner. 
``Term``, None , *colum* , *data*
    Adds a term for your. *name* will be the label for this bar. 
    *columns* is a "$"-separated variable that refers to the columns 
    accessed in the data (e.g. 2$3$4 accesses columns 2-4 in the dataset). 
    *color* refers to the rgb values that are ";"-separated (e.g. 155;155;155).


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


The Panel Parameter Type
^^^^^^^^^^^^^^^^^^^^^^^^

Description
+++++++++++

This file specifies the layout of the panel.
Since the panel can contain multiple figures, 
you can specify the width and height of the figures 
and how many figures per row.
You will also specify here the information that goes
in the tabs, which is included in all panels. 
Note that these websites have responsive designs, 
so the actual width will change as the user changes the 
size of the window. To accomodate this, we will represent
width as the percent width of the window. 

This parameter type also has a START term, to divide
the unordered and the orderd variables as discussed above.

Unordered Variables
+++++++++++++++++++

``panelkey``
    A unique name for your panel that will be used
    to reference the panel in other parameter types.
``setname``
    The text that you would like displayed as the header of
    the info section in the tabs. 
``info``
    The text that you would like displayed in the info section. 
``citetext``
    The text that you would like displayed in the citation section 
    of the tabs.
``citelink``
    The webpage that you would like forwarded when a user
    clicks the citetext. 

Ordered Variables
+++++++++++++++++

``START``
    Specifies that the subsequent terms 
    should be ordered in the corresponding manner.
``FIGURE``, *figurekey*, *widthpct*, *har*, *rownum*, *colnum*
    Denotes the addition of a figure. 
    *figurekey* should match the figurekey in the figure parameter
    file for the figure that you would like to display. 
    *widthpct* is the percent width (1-100) of the panel
    that the figure should take up. 
    *har* can be either the height in pixels (just a number), 
    or it can be in the format R(ar) where "ar" refers to the
    aspect ratio that you would like to maintain. See the
    advanced section for more details. 
    *rownum* is the row number for the figure in the 
    panel. The first row should be 1.
    *colnum* is the col number for the figure in the panel. 
    Leftmost colnum should be 1.

Example
+++++++

::

    citetext	"Allen Human Brain Atlas
    Hawrylycz, M.J. et al. (2012) An anatomically comprehensive atlas of the adult human transcriptome, Nature 489: 391-399. doi: 10.1038/nature11405"				
    citelink	http://www.alleninstitute.org/				
    setname	Association between Age and Gene Expression				
    info	This data shows expression levels in brain with varying ages. 				
    START					
    FIGURE,	agetitle,	100	200, 1,	1
    FIGURE, agebarplot, 100, 400, 2, 1
    FIGURE,	ageboxplot,	50	400, 3,	1
    FIGURE,	ageviolin,	50	400, 3,	2




Troubleshooting
^^^^^^^^^^^^^^^

- All of the files should be in one folder. 
- Files can be either .csv, .txt, or .xlsx. 
- .txt files should be Tab-delimited. 
- If you are using Excel, only the first sheet of each .xlsx file will be used. 
