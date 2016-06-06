import networkx as nx
import json
import matplotlib.pyplot as plt
from collections import Counter

# Force matplotlib to not use any Xwindows backend.
# plt.use('Agg')

# with open('data.json') as infile:
#     data = json.load(infile)

def buildnetwork(resources):
    """
    Create graph file from resource data.
    """

    set_with_disciplines = {
        'http://dbpedia.org/resource/Category:Culinary_arts',
        # 'http://dbpedia.org/resource/Category:Social_sciences',
        # 'http://dbpedia.org/resource/Category:Humanities',
        # 'http://dbpedia.org/resource/Category:Science',
        'http://dbpedia.org/resource/Category:Biology',
        'http://dbpedia.org/resource/Category:Musicology',
        'http://dbpedia.org/resource/Category:Physics',
        'http://dbpedia.org/resource/Category:Chemistry',
        'http://dbpedia.org/resource/Category:Philosophy',
        'http://dbpedia.org/resource/Category:Geography',
        'http://dbpedia.org/resource/Category:Anthropology',
        'http://dbpedia.org/resource/Category:Archaeology',
        'http://dbpedia.org/resource/Category:Economics',
        'http://dbpedia.org/resource/Category:History',
        'http://dbpedia.org/resource/Category:Philology',
        'http://dbpedia.org/resource/Category:Psychology',
        'http://dbpedia.org/resource/Category:Law',
        'http://dbpedia.org/resource/Category:Religion',
        'http://dbpedia.org/resource/Category:Mathematics',
        'http://dbpedia.org/resource/Category:Health',
        'http://dbpedia.org/resource/Category:Sports'
        
    }

    for URI_NL in resources:
        resources[URI_NL]['disciplines'] = []
        if resources[URI_NL].get('routelist'):        
            routelist = resources[URI_NL]['routelist'][0]
            for category in set_with_disciplines:
                for lst in routelist:
                    if category in lst:
                        resources[URI_NL]['disciplines'].append(category)
        else:
            continue

    # G0=nx.Graph()
    # plt.figure(figsize=(30,30))

    # for key in data.keys():
    #     #G0.add_node(key)
    #     setofdisciplines = set(data[key]['disciplines'])
    #     for discipline in setofdisciplines:
    #         if discipline:
    #             G0.add_edge(key,discipline)
            
    G0=nx.Graph()
    #G.add_nodes_from(data.keys())

    for key in resources.keys():
        #G0.add_node(key, weight=len(resources[key]['offset']))

        weight = len(resources[key]['offset'])

        setofdisciplines = set(resources[key]['disciplines'])
        for discipline in setofdisciplines:
            if discipline:
                G0.add_edge(key,discipline, weight=weight)
            # else:
            #     G0.add_node(key)
                


    nx.draw(G0, with_labels=True)

    nx.write_gml(G0,"output/network.gml")

    return resources