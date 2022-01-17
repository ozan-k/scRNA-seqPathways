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

tissue_types = ['EpiA', 'EpiB', 'LPA', 'LPB']

def mergeAndTakeMean(path):
    l = 0
    dct = {}
    tissue_types = get_current_items_in(path)
    for tt in tissue_types:
        files = get_current_items_in(path+"/"+tt)
        # print(files)
        for f in files:    
            l+=1
            data = get_data(path+"/"+tt+"/"+f)
            for item in data:
                if item in dct:
                    dct[item]['read'] += int(data[item]['read'])
                else:
                    dct[item] = { "read": int(data[item]['read']), "count": data[item]['count']}
    for item in dct:
        dct[item]["read"] = dct[item]["read"]/l
    return dct

def takeDiff(main,second,cell_type):
    path_beginning = "../ModelBuilder/TranscriptomicsData/"
    dct = {}
    path_end = "/" + cell_type + "/"
    main_dct = mergeAndTakeMean(path_beginning+main+path_end)
    second_dct = mergeAndTakeMean(path_beginning+second+path_end)
    for item in main_dct:
        if item in second_dct:
            diff = main_dct[item]["read"] - second_dct[item]["read"]
            if diff > 0: 
                dct[item] = diff
        else:
            dct[item] = main_dct[item]["read"]
    with open("Molecules"+ main+"/"+cell_type+".json", 'w') as outfile:
        json.dump(dct, outfile)         
    return dct

cell_types = ['Best4+ Enterocytes', 'CD4+ Activated Fos-hi', 'CD4+ Activated Fos-lo', 'CD4+ Memory', 'CD4+ PD1+', 'CD69+ Mast', 'CD69- Mast', 'CD8+ IELs', 'CD8+ IL17+', 'CD8+ LP', 'Cycling B', 'Cycling Monocytes', 'Cycling T', 'Cycling TA', 'DC1', 'DC2', 'Endothelial', 'Enterocyte Progenitors', 'Enterocytes', 'Enteroendocrine', 'Follicular', 'GC', 'Glia', 'Goblet', 'ILCs', 'Immature Enterocytes 1', 'Immature Enterocytes 2', 'Immature Goblet', 'Inflammatory Fibroblasts', 'Inflammatory Monocytes', 'M cells', 'MT-hi', 'Macrophages', 'Microvascular', 'Myofibroblasts', 'NKs', 'Pericytes', 'Plasma', 'Post-capillary Venules', 'RSPO3+', 'Secretory TA', 'Stem', 'TA 1', 'TA 2', 'Tregs', 'Tuft', 'WNT2B+ Fos-hi', 'WNT2B+ Fos-lo 1', 'WNT2B+ Fos-lo 2', 'WNT5B+ 1', 'WNT5B+ 2']
for item in cell_types:
    print(item)
    takeDiff("Non-inflamed","Healthy",item)

