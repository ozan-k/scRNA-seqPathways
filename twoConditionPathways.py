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

def convert_to_dct(lst):
    return { k[1] : [k[0],k[2]] for k in lst }
 

def processFiles(file_name_prefix,file):
    dataHealthy = convert_to_dct(get_data(file_name_prefix+"/Healthy/"+file + "_pathways.json"))
    dataInflamed = convert_to_dct(get_data(file_name_prefix+"/Inflamed/"+file + "_pathways.json"))
    dataNoninflamed = convert_to_dct(get_data(file_name_prefix+"/Non-inflamed/"+file + "_pathways.json"))
    all_keys = list(dict.fromkeys(list(dataHealthy.keys())+list(dataInflamed.keys())+list(dataNoninflamed.keys())))
    lst = []
    for k in all_keys:
        if k in dataNoninflamed and not k in dataInflamed and k in dataHealthy:
            l = []
            # l.append((dataInflamed[k][0],"I"))
            l.append((dataNoninflamed[k][0],"N"))
            l.append((dataHealthy[k][0],"H"))
            l.sort()
            l = [l[1][0]/l[0][0]] + l 
            l.append(dataNoninflamed[k][1])
            lst.append(l)
            # print(k,dataHealthy[k])
    lst.sort(reverse=True)
    return lst        

# state_list = ["Healthy"]
# cell_types = ['Best4+ Enterocytes']

cell_types = ['Best4+ Enterocytes', 'CD4+ Activated Fos-hi', 'CD4+ Activated Fos-lo', 'CD4+ Memory', 'CD4+ PD1+', 'CD69+ Mast', 'CD69- Mast', 'CD8+ IELs', 'CD8+ IL17+', 'CD8+ LP', 'Cycling B', 'Cycling Monocytes', 'Cycling T', 'Cycling TA', 'DC1', 'DC2', 'Endothelial', 'Enterocyte Progenitors', 'Enterocytes', 'Enteroendocrine', 'Follicular', 'GC', 'Glia', 'Goblet', 'ILCs', 'Immature Enterocytes 1', 'Immature Enterocytes 2', 'Immature Goblet', 'Inflammatory Fibroblasts', 'Inflammatory Monocytes', 'M cells', 'MT-hi', 'Macrophages', 'Microvascular', 'Myofibroblasts', 'NKs', 'Pericytes', 'Plasma', 'Post-capillary Venules', 'RSPO3+', 'Secretory TA', 'Stem', 'TA 1', 'TA 2', 'Tregs', 'Tuft', 'WNT2B+ Fos-hi', 'WNT2B+ Fos-lo 1', 'WNT2B+ Fos-lo 2', 'WNT5B+ 1', 'WNT5B+ 2']

def iter():
    input_prefix = "./4_Aggregated_Pathways" 
    for file in cell_types:
        result = processFiles(input_prefix,file)
        outputfile = "./Pathways__Healthy_and_Noninflamed/"+file
        print(outputfile)
        with open(outputfile+ "_pathways_in_noninflamed_and_healthy.json", 'w') as outfile:
            json.dump(result, outfile)    


iter()



