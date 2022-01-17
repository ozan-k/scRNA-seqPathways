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
    query0 = 'MATCH (pe:PhysicalEntity{stId:"'+ stId +'"})'
    #query0 += '<-[:input|output|catalystActivity|physicalEntity|regulatedBy|regulator|hasComponent|hasMember|hasCandidate*]-'
    query0 += '<-[:output]-'
    query0 += '(r:ReactionLikeEvent) '
    query0 += 'RETURN DISTINCT r.stId' 
    result = transaction.run(query0)
    result = [ json.dumps(r).split("\"")[1] for r in result]
    return result


def getMoleculeData(stId):
    with driver.session() as session:
        result = session.read_transaction(get_Reactome_stId, stId)
        return result

def processFile(fileName):
    data = get_data(fileName)
    dct = {}
    for item in data:
        reactions = getMoleculeData(item)
        if reactions != []:
            dct[item] = {"reactions": reactions, "read" :data[item]["read"]}
    return dct        



def iter():
    health_types = ["Healthy", "Inflamed", "Non-inflamed"]
    for folder in health_types:
        cell_types = get_current_items_in("../ModelBuilder/TranscriptomicsData/"+folder)
        for ct in cell_types:
            tissues = get_current_items_in("../ModelBuilder/TranscriptomicsData/"+folder+"/"+ct)
            for tissue in tissues:
                files = get_current_items_in("../ModelBuilder/TranscriptomicsData/"+folder+'/'+ct+"/"+tissue)
                for file in files:
                    inputfile = "../ModelBuilder/TranscriptomicsData/"+folder+"/"+ct+"/"+tissue +"/"+file
                    result = processFile(inputfile)
                    outputfile = "./MoelculeReactions/"+folder+"/"+ct+"/"+tissue +"/"+file
                    print(outputfile)
                    with open(outputfile[:-5]+ "_moleculeReactions.json", 'w') as outfile:
                        json.dump(result, outfile)    

                
iter()

    

def produceFolders():
    health_types = ["Healthy", "Inflamed", "Non-inflamed"]
    for folder in health_types:
        os.mkdir("./MoelculeReactions/"+folder)
        cell_types = get_current_items_in("../ModelBuilder/TranscriptomicsData/"+folder)
        for ct in cell_types:
            os.mkdir("./MoelculeReactions/"+folder+"/"+ct)
            tissues = get_current_items_in("../ModelBuilder/TranscriptomicsData/"+folder+"/"+ct)
            for tissue in tissues:
                os.mkdir("./MoelculeReactions/"+folder+"/"+ct+"/"+tissue)
