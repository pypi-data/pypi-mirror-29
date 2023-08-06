#!/usr/bin/env python2.7

from __future__ import print_function


'''


#NOTE - we need to store everything in base64 encoding or UNICODE! otherwise, the data looks weird. 

'''

from google.cloud import datastore

def upload_dataset2datastore(filepath, client, datasetkey, searchcol, searchrowstart, numrow="all"):
    print("Uploading data to datastore from location: ", filepath)
    print("This step can take a long time.")
    print("\tNumber of rows to upload: ", numrow)
    if filepath[-5:] ==".xlsx":
        add_file_to_datastore_xls(filepath,  client, datasetkey, searchcol, searchrowstart, numrow )
    else:
        add_file_to_datastore_csvtxt(filepath,  client, datasetkey, searchcol,searchrowstart, numrow)
                
def add_file_to_datastore_csvtxt(filepath, client,  datasetkey, searchcol, searchrowstart, numrow):
    counter =0
    tasklist = list()
    with open(filepath) as F:
        for i in range(int(searchrowstart)-1):
            F.readline()
        for i in F:
            if filepath[-4:]==".txt":
                univec =unicode(i).rstrip().split("\t")
            elif filepath[-4:]==".csv":
                univec =unicode(i).rstrip().split(",")
            else: 
                print("ERROR, FILES NEED TO END IN .txt, .csv, .xlsx AND BE IN THE CORRESPONDING FORMAT")
            task = create_dataset_entity(client, unicode(datasetkey), univec[int(searchcol)-1],univec)
            tasklist.append(task)
            if len(tasklist)>400: 
                add_dataset_entity(client, tasklist)
                tasklist = list()
            counter +=1
            if counter%100==0: print(counter)
            if numrow!="all" and counter==int(numrow): break
    add_dataset_entity(client, tasklist)
          
def add_file_to_datastore_xls(filepath, client, datasetkey, searchcol, searchrowstart, numrow):
    counter =0
    tasklist = list()
    import xlrd
    xl_workbook = xlrd.open_workbook(filepath)
    xl_sheet = xl_workbook.sheet_by_index(0)
    startRowIndex = int(searchrowstart)-1
    endRowIndex = xl_sheet.nrows
    num_cols = xl_sheet.ncols  
    outMat = list()
    for row_idx in range(startRowIndex, endRowIndex):    # Iterate through rows
        univec = list()
        for col_idx in range(num_cols):  # Iterate through columns
            cell_obj = xl_sheet.cell(row_idx, col_idx)  # Get cell object by row, col
            univec.append(unicode(cell_obj.value))
        task = create_dataset_entity(client, unicode(datasetkey), univec[int(searchcol)-1], univec)
        tasklist.append(task)
        if len(tasklist)>400: 
            add_dataset_entity(client, tasklist)
            tasklist = list()
        counter +=1
        if counter%100==0: print(counter)
        if numrow!="all" and counter==int(numrow): break
    add_dataset_entity(client, tasklist)

def create_dataset_entity(client, datasetkey, searchterm, datalist):
    '''
    This creates a datastore entity with a single index called searchterm.  
    '''
    key = client.key(datasetkey)

    task = datastore.Entity(
        key, exclude_from_indexes=['data']
        )

    task.update({
        'searchTerm': searchterm,
        'data': datalist,
    })
    return task

def add_dataset_entity(client, tasklist):
    client.put_multi(tasklist)

def test_production_datastore(appid, datasetkey, searchTerm ):
    client = datastore.Client(appid) 
    query = client.query(kind=datasetkey)
    query.add_filter('searchTerm', '=', unicode(searchTerm))
    for i in query.fetch(1):
        print(i)
