Step 1: Creating your input files
=================================

Overview
^^^^^^^^

You will first need to supply the data that your website will use.
In addition, you will need to create a parameter file (in Excel or a text editor) that specifies how the webpage will look.
Here, we will talk about what format your data files should be
and how to create your parameter file. 

This step can take the longest (> 10 minutes, depending 
on your website design). 

Tutorial/Quickstart
^^^^^^^^^^^^^^^^^^^

For getting a tutorial website running quickly: 

- You can download an example dataset and parameter file `here <http://www.dataspectra.org/tutorial.zip>`_.
- After double-clicking to extract the file, you will find a tutorial_files folder. 
- The tutorial_files contains a data file (ds.tutorial.data.csv) and a complete parameter file (ds.tutorial.parameters.xlsx).
- To simply test dataspectra, you can use these and skip to Step 2.
- For the uninitiated, I would recommend opening these files and taking a look to see what they look like.  

For building your own website:

- I would recommend starting off with getting a tutorial up and running. 
- Then, take a look at the template file (ds.tutorial.parameters.template.xlsx) included with the tutorial material. 
- You can fill in the parameters and delete unnecessary parts as needed. 

Tutorial File Contents:

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
The datafiles can be .csv (comma-separated) or .txt (tab-delimited) format. 

Primary search terms
    The terms that your user will search for in your website.

Parameter File Overview
^^^^^^^^^^^^^^^^^^^^^^^

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
Take a look at the tutorial file - ds.tutorial.parameters.xlsx 
(download `here <http://www.dataspectra.org/tutorial.zip>`_) - to see what it looks like. 

A template parameter file is also included (ds.parameter.template.xlsx)
to guide you in creating your own parameter file.

A few notes:

- The columns should be separated by Excel boxes, commas, or tabs depending 
  on the type of file you're saving it as. 
- Make sure to save the file with the appropriate suffix 
  (.csv for commas-separated columns, .txt for tab-separated columns,
  and .xlsx for Excel files) 
- If you are going to save a comma-separated file,
  make sure to not include any commas within a particular 
  text column. 
- Unless otherwise specified, the variables for each parameter file should be
  in the file format as (for e.g. in a csv file) ::
    variablename,The name of your variable
    variablekey,The variable key that you want to use
- When specifying a new parameter type (e.g. a new figure, dataset, or panel)
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
    toplink,http://www.dataspectra.org
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

    parameter,sidebar
    START		
    SEARCH,SEARCH	
    SPACE		
    PANEL,Age,agepanel
    PANEL,Distributions,distributionpanel


The Figure parameter type
^^^^^^^^^^^^^^^^^^^^^^^^^

Description
+++++++++++

The figure parameter type encompasses all objects 
in the panel. This includes plots and titles. 
For each figure, you will need to create a separate 
figure parameter type. This section instructs how each 
figure accesses the data and how it is plotted. 
Because there a number of types of figures, we will 
only describe the format for two types - the title figure,
and the barplot figure. The title figure will display a specific
column of text from your dataset. We will use it to display the 
search term. Check out "Parameters" link for more
detail on the other plots.

Here, we also have the START term, which will be used 
in your figure parameter type to distinguish the 
variables from the ordered rows. 

The unordered variables will go first, 
and then the START term, and lastly the ordered rows. 
As the name suggests, the order of the ordered 
rows will be used in the panel.

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

Ordered variables (for barplot)
+++++++++++++++++++++++++++++++

``START``
    Specifies that the subsequent terms 
    should be ordered in the corresponding manner. 
``BAR``, *name* , *columns* , *datarow*, *color*
    Adds a bar to your plot. 
    *name* will be the label for this bar.
    *columns*  can be specified by "-", where 2-4 will refer to the columns
    2,3 and 4. Individual columns can also be specified with a "$" separation (e.g. 2$3$4 accesses columns 2-4 in the dataset). 
    *color* is specified with rgb values that are ";"-separated and surrounded by parantheses. (e.g. (155;155;155)).
    *datarow*  is the dataset row that will be used for this element. Put "data" here, unless you are using a metadata file.
``SPACE``
    Adds an empty space next to the bar. 

Example  
+++++++ 

::

    parameter,figure
    figurekey,mybarplot
    figuretype,barplot
    valuelabel,FPKM
    title,Expression in brain
    datasetkey,braindata
    START
    BAR,Astrocytes,2-4,data,(155;155;155)
    BAR,Neurons,5-7,data,(155;155;155)
    BAR,Microglia,8-10,data,(155;155;155)
    SPACE
    BAR,Total,11-13,data,(155;155;155)


Ordered variables (for title)
++++++++++++++++++++++++++++++

``START``
    Specifies that the subsequent terms 
    should be ordered in the corresponding manner. 
``TEXT``, None , *columns* , *datarow*, *color*
    Adds a term for your. *name* will be the label for this bar. 
    *columns* - put here the column from the dataset that you want displayed. Usually 1, if you search term is the first column of your dataset.
    *datarow* is the dataset row that will be used for this element. Put "data" here, unless you are using a metadata file.
    *color* is specified with rgb values that are ";"-separated and surrounded by parantheses. (e.g. 155;155;155).

Example
+++++++

::

    parameter, figure	
    figurekey,agetitle			
    figuretype,title			
    datasetkey,brainspandata			
    START				
    TEXT,None,1,data,(0;0;0)



The Panel Parameter Type
^^^^^^^^^^^^^^^^^^^^^^^^

Description
+++++++++++

This parameter type specifies the layout of the panel.
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

    parameter,panel
    panelkey,agepanel
    citetext,Allen Human Brain Atlas; Hawrylycz M.J. et al. (2012) An anatomically comprehensive atlas of the adult human transcriptome; Nature 489: 391-399. doi: 10.1038/nature11405				
    citelink,http://www.alleninstitute.org/				
    setname,Association between Age and Gene Expression				
    info,This data shows expression levels in brain with varying ages. 				
    START					
    FIGURE,agetitle,100,200,1,1
    FIGURE,agebarplot,100,400,2,1
    FIGURE,ageboxplot,50,400,3,1
    FIGURE,ageviolin,50,400,3,2


Troubleshooting
^^^^^^^^^^^^^^^

- All of the files should be in one folder. 
- Files can be either .csv, .txt, or .xlsx. 
- .txt files should be Tab-delimited. 
- If you are using Excel, only the first sheet of each .xlsx file will be used. 
