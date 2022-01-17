#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from neo4j import GraphDatabase
import json
import os

def get_current_items_in(this_path):
    item_list = os.listdir(this_path)
    item_list.sort()
    if '.DS_Store' in item_list:
        item_list.remove('.DS_Store')
    if 'desktop.json' in item_list:
        item_list.remove('desktop.json')
    return item_list

def get_data(file_name):
    with open(file_name,encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data

# connection details for the neo4j database
uri = "neo4j://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4j"))
def get_Reactome_stId(transaction, stId):
    query0 = 'MATCH (x:Pathway{stId:"'+ stId +'"}) '
    query0 += 'RETURN x.displayName' 
    result = transaction.run(query0)
    for r in result:
        r = json.dumps(r).split("\"")[1]
        break
    return r

def getMoleculeData(stId):
    with driver.session() as session:
        result = session.read_transaction(get_Reactome_stId, stId)
        return result

def processFile(fileName):
    data = get_data(fileName)
    lst = []
    for k,item in enumerate(data):
        name = getMoleculeData(item[0])
        lst.append([name]+item)
    return lst        

# state_list = ["Healthy"]
# cell_types = ['Best4+ Enterocytes']

state_list = ["Healthy","Inflamed","Non-inflamed"]
cell_types = ['Best4+ Enterocytes', 'CD4+ Activated Fos-hi', 'CD4+ Activated Fos-lo', 'CD4+ Memory', 'CD4+ PD1+', 'CD69+ Mast', 'CD69- Mast', 'CD8+ IELs', 'CD8+ IL17+', 'CD8+ LP', 'Cycling B', 'Cycling Monocytes', 'Cycling T', 'Cycling TA', 'DC1', 'DC2', 'Endothelial', 'Enterocyte Progenitors', 'Enterocytes', 'Enteroendocrine', 'Follicular', 'GC', 'Glia', 'Goblet', 'ILCs', 'Immature Enterocytes 1', 'Immature Enterocytes 2', 'Immature Goblet', 'Inflammatory Fibroblasts', 'Inflammatory Monocytes', 'M cells', 'MT-hi', 'Macrophages', 'Microvascular', 'Myofibroblasts', 'NKs', 'Pericytes', 'Plasma', 'Post-capillary Venules', 'RSPO3+', 'Secretory TA', 'Stem', 'TA 1', 'TA 2', 'Tregs', 'Tuft', 'WNT2B+ Fos-hi', 'WNT2B+ Fos-lo 1', 'WNT2B+ Fos-lo 2', 'WNT5B+ 1', 'WNT5B+ 2']

def iter(state):
    for file in cell_types:
        inputfile = "./3_Sorted_Pathways/Molecules"+state+"/"+file + "_CatReg_pathways.json"
        result = processFile(inputfile)
        outputfile = "./"+state+"/"+file
        print(outputfile)
        with open(outputfile+ "_CatReg_pathways.json", 'w') as outfile:
            json.dump(result, outfile)    


for item in state_list:
    iter(item)



