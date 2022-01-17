#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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


def processFile(data):
    def sortSecond(val):
        return val[1] 
    dct = {}
    for reaction in data:
        for pathway in data[reaction]["pathways"]:
            if pathway in dct:
                dct[pathway]+= data[reaction]["read"]
            else:
                dct[pathway] = data[reaction]["read"]
    lst = list(dct.items())
    lst.sort(key=sortSecond,reverse=True) 
    return lst

state_list = ["Healthy","Inflamed","Non-inflamed"]
cell_types = ['Best4+ Enterocytes', 'CD4+ Activated Fos-hi', 'CD4+ Activated Fos-lo', 'CD4+ Memory', 'CD4+ PD1+', 'CD69+ Mast', 'CD69- Mast', 'CD8+ IELs', 'CD8+ IL17+', 'CD8+ LP', 'Cycling B', 'Cycling Monocytes', 'Cycling T', 'Cycling TA', 'DC1', 'DC2', 'Endothelial', 'Enterocyte Progenitors', 'Enterocytes', 'Enteroendocrine', 'Follicular', 'GC', 'Glia', 'Goblet', 'ILCs', 'Immature Enterocytes 1', 'Immature Enterocytes 2', 'Immature Goblet', 'Inflammatory Fibroblasts', 'Inflammatory Monocytes', 'M cells', 'MT-hi', 'Macrophages', 'Microvascular', 'Myofibroblasts', 'NKs', 'Pericytes', 'Plasma', 'Post-capillary Venules', 'RSPO3+', 'Secretory TA', 'Stem', 'TA 1', 'TA 2', 'Tregs', 'Tuft', 'WNT2B+ Fos-hi', 'WNT2B+ Fos-lo 1', 'WNT2B+ Fos-lo 2', 'WNT5B+ 1', 'WNT5B+ 2']

def iter(state):
    for file in cell_types:
        inputfile = "./Reactions_to_pathways/Molecules"+state+"/"+file + "_CatReg_pathways.json"
        outputfile = "./Molecules"+state+"/"+file 
        data = get_data(inputfile)
        result = processFile(data)
        print(outputfile)
        with open(outputfile+ "_CatReg_pathways.json", 'w') as outfile:
            json.dump(result, outfile)    

for item in state_list:
    iter(item)

