import time
import pickle
from SPARQLWrapper import SPARQLWrapper, JSON

def getEnglishURI(URI):
    """Nederlandse URI erin, Engelse (algemene) eruit."""

    global EN_URIdict

    if URI in EN_URIdict:
        return EN_URIdict[URI]
    else:
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery("""
            SELECT ?a 
            WHERE {
            ?a owl:sameAs <%s>.
            }
            """ % URI )
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        time.sleep(.05) #to not nuke the DBpedia endpoint.

        for result in results["results"]["bindings"]:
            URI_EN = result["a"]["value"]
            EN_URIdict[URI] = URI_EN
            return(URI_EN)


def getsubjects(URI_EN):
    """
    Returns all values from DBpedia categories dct:subject as a list.
    """

    if URI_EN in subjects_URIdict:
        return subjects_URIdict[URI_EN]
    else:
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery("""
            SELECT ?a 
            WHERE {        
            <%s> dct:subject ?a.
            }
            """ % URI_EN )
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        time.sleep(.05) #to not nuke the DBpedia endpoint.

        subjectlist = []
        
        for result in results["results"]["bindings"]:
            subjectlist.append((result["a"]["value"]))
        
        subjects_URIdict[URI_EN] = subjectlist
        return subjectlist
    

def addEnglishURItodict(d):
    """
    Adds general DBpedia URI to dictionary under key 'URI_EN'
    """
    
    for URI_NL in d.keys():
        
        URI_EN = getEnglishURI(URI_NL)        
        d[URI_NL]['URI_EN'] = URI_EN
        
    return d


def addsubjecttodict(d):
    """
    Adds DBpedia subjects to dictionary under key 'subjects'
    """
    
    for URI_NL in d.keys():
        
        URI_EN = d[URI_NL]['URI_EN']        
        subjects = getsubjects(URI_EN)
        
        d[URI_NL]['subjects'] = subjects
        
    return d


def getbroader(URI, endpoint):
    """
    Local version.
    Returns the broader concepts (skos: broader) from
    an URI from the DBpedia dump. 
    """

    global URI_broaderdict

    if URI in URI_broaderdict.keys():
        broaderlist = URI_broaderdict[URI]
    else:   
        broaders = endpoint.query("""
            SELECT ?a 
            WHERE {        
                <%s> <http://www.w3.org/2004/02/skos/core#broader> ?a. 
                }
            """ % URI )
        
        broaderlist = []
        for item in broaders:
            broaderlist.append('%s' % item)

        URI_broaderdict[URI] = broaderlist
    
    return broaderlist


def findtoplevel(URI, top_level, endpoint, maxdepth):
    """
    Returns a list of routes to a value in the top_level list. 
    """
    depth = 1
    
    route = []
    route.append(URI)
    
    # get all broaders for the URI subject
    broaderlist = getbroader(URI, endpoint)
    
    # if the top level is reached
    if not top_level.isdisjoint(broaderlist):

        hit = list(set(top_level) & set(broaderlist))

        return hit
    else:
        return recursive(broaderlist, route, top_level, depth, endpoint, maxdepth)
        
    
def recursive(URI_list, route, top_level, depth, endpoint, maxdepth):
    """
    Recursive function to be used in findtoplevel().
    Returns a list containing the route of URI's to the 
    most abstract discipline. 
    """
    # counter
    if depth > maxdepth:
        return ''
    else:
        depth += 1
    
    setofbroader = set()
    setofbroader.clear()
    
    results = []
    
    for broader in URI_list:
        broaderlist = getbroader(broader, endpoint)
        
        route.append(broader)
        
        # if the URI shares broaders with the top_level list, add it
        if not top_level.isdisjoint(broaderlist):

            hit = list(set(top_level) & set(broaderlist))
            route.append(hit)

            #return route
            results.append(route)
            
        else:
            setofbroader.update(broaderlist)
            #print(setofbroader)
            
    if results:
        return results
    else:
        try:
            return recursive(setofbroader, route, top_level, depth, endpoint, maxdepth)
        except:
            return ''

    
def makeroute(URI_NL, top_level, d, endpoint, maxdepth):
    """
    IN: URI_NL
    OUT: route of URI's as list 
    """
    resultlist = []
    
    #URI_EN = getEnglishURI(URI_NL)
    URI_EN = d[URI_NL]['URI_EN']
    
    list_of_subjects = d[URI_NL]['subjects']
    

    
    for subject in list_of_subjects:
        resultlist.append(findtoplevel(subject, top_level, endpoint, maxdepth))
        #return findtoplevel(subject, top_level)
        
    return resultlist
        

def loadURIdatasets():
    """Load saved dbpedia data for quicker lookup."""

    global URI_broaderdict
    global EN_URIdict
    global subjects_URIdict

    try:
        with open('datasets/URI_broaderdict.pickle', 'rb') as infile:
            URI_broaderdict = pickle.load(infile)
            print("Loaded URI_broaderdict!")
    except:
        URI_broaderdict = dict()


    try:
        with open('datasets/EN_URIdict.pickle', 'rb') as infile:
            EN_URIdict = pickle.load(infile)
            print("Loaded EN_URIdict!")
    except:
        EN_URIdict = dict()


    try:
        with open('datasets/subjects_URIdict.pickle', 'rb') as infile:
            subjects_URIdict = pickle.load(infile)
            print("Loaded subjects_URIdict!")
    except:
        subjects_URIdict = dict()

def dumpURIdatasets():
    """
    Store acuired dbpedia data into pickles for future use (=quicker).
    """

    global URI_broaderdict
    global EN_URIdict
    global subjects_URIdict

    with open('datasets/URI_broaderdict.pickle', 'wb') as outfile:
        pickle.dump(URI_broaderdict, outfile)

    with open('datasets/EN_URIdict.pickle', 'wb') as outfile:
        pickle.dump(EN_URIdict, outfile)

    with open('datasets/subjects_URIdict.pickle', 'wb') as outfile:
        pickle.dump(subjects_URIdict, outfile)

        


        