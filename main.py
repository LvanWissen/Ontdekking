import requests
import pickle
import re
import json

from collections import defaultdict
from rdflib import Graph
from dbpedia import *
from network import *

#set arguments for spotlight extractor
confidence = 0.2
support = 0

#set maximmum depth for recursive dbpedia skos broader function
maxdepth = 400


def spotlight(text_data, offset_total, resources):
    """
    Takes input and returns a dictionary with annotation data. 
    """

    #parameters spotlight
    args = {"text": text_data, "confidence":confidence, "support": support}
    headers = {"Accept": "application/json", "content-type":"application/x-www-form-urlencoded"}
    # URL = ("http://spotlight.sztaki.hu:2232/rest/annotate") #abuse the public endpoint
    URL = "http://10.10.1.2:2222/rest/annotate" #local version. See: https://github.com/dbpedia-spotlight/dbpedia-spotlight/wiki/Run-from-a-JAR

    #requests
    r = requests.post(URL, params=args, headers=headers)
    r.encoding = 'cp1252'

    annotation_json = json.loads(r.text)

    if "Resources" in annotation_json.keys():
        for resource in annotation_json["Resources"]:
            URI = resource["@URI"]
            offset = int(resource["@offset"])
            surfaceform = resource["@surfaceForm"]

            resources[URI]["surfaceform"].append(surfaceform)
            resources[URI]["offset"].append(offset + offset_total)

    return resources


def spotlight_feeder(textfile, stepsize=20, windowsize=20):
    """
    Returns dictionairy with URI and offset information.
    """
    offset_total = 0
    resources = defaultdict(lambda: defaultdict(list))


    with open(textfile, encoding="utf-8") as infile:
        sentences = re.split('\n', infile.read())


    for i in range(0, (len(sentences)-windowsize+stepsize), stepsize):

        #create text size of n_windowsize sentences
        window = sentences[i:i+windowsize]

        textsize = len(" ".join(window[:stepsize])) + 1 #space

        window_string = " ".join(window)

        resources = spotlight(window_string, offset_total, resources)
        offset_total += textsize

    return resources








if __name__ == '__main__':

    # print("Annotating text...")
    # resources = spotlight_feeder('text/OntdekkingVanDeHemel_zinnen_utf8.txt')
    # print("Done.")
    # json.dump(resources, open('output/data_raw.json', 'w', encoding='utf-8'), indent=4)

    resources = json.load(open('output/data_raw.json', 'r', encoding='utf-8'))

    print("Number of entities:", len(resources.keys()))

    print("Loading datastore...")
    with open('datasets/skos.pickle', 'rb') as infile:
        skos = pickle.load(infile)
    print("Done.")

    print("Loading URI_broaderdict...")
    loadURIdatasets()
    print("Done.")

    print("Getting English URIs...")
    addEnglishURItodict(resources)
    print("Done.")

    print("Getting subjects...")
    addsubjecttodict(resources)
    print("Done.")

    print("Getting broader categories...")

    top_level = {
                'http://dbpedia.org/resource/Category:Disciplines'
              }

#     top_level = {
#     'http://dbpedia.org/resource/Category:Culinary_arts',
#     'http://dbpedia.org/resource/Category:Biology',
#     'http://dbpedia.org/resource/Category:Musicology',
#     'http://dbpedia.org/resource/Category:Physics',
#     'http://dbpedia.org/resource/Category:Chemistry',
#     'http://dbpedia.org/resource/Category:Philosophy',
#     'http://dbpedia.org/resource/Category:Geography',
#     'http://dbpedia.org/resource/Category:Anthropology',
#     'http://dbpedia.org/resource/Category:Archaeology',
#     'http://dbpedia.org/resource/Category:Economics',
#     'http://dbpedia.org/resource/Category:History',
#     'http://dbpedia.org/resource/Category:Philology',
#     'http://dbpedia.org/resource/Category:Psychology',
#     'http://dbpedia.org/resource/Category:Law',
#     'http://dbpedia.org/resource/Category:Religion',
#     'http://dbpedia.org/resource/Category:Mathematics',
#     'http://dbpedia.org/resource/Category:Health',
#     'http://dbpedia.org/resource/Category:Sports',
#     'http://dbpedia.org/resource/Category:Disciplines'
# }

    # counter
    n=0

    # add the routelist to the dictionary resources
    n_total = len(resources.keys())
    for key in resources.keys():
        n+=1
        print("%d/%d %s" % (n, n_total, key))

        resources[key]['routelist'] = makeroute(key, top_level, resources, skos, maxdepth)

    print("Done.")

    # print("Loading datasets...")
    # skos = Graph()
    # skos.parse('datasets/skos_categories_en.ttl', format='n3')
    # print("Done.")

    # with open('datasets/skos.pickle', 'wb') as outfile:
    #     pickle.dump(skos, outfile)

    #store datasets
    print("Saving datasets for future use...")
    dumpURIdatasets()
    print("Done.")
    
    #networkx
    print("Creating network...")
    resources = buildnetwork(resources)
    print("Done.")

    #store data in json
    print("Saving data to json...")
    json.dump(resources, open('output/data.json', 'w', encoding='utf-8'))
    print("Done.")








