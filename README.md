# Discovering the encyclopaedic novel
A case study in automatically analysing Harry Mulisch’s _The Discovery of Heaven_ (1992)

More information about this project is described in the abstract that was presented at the DHBenelux2016 conference in Belval, Luxembourg: 

Van Wissen, Leon, Marieke van Erp, and Ben Peperkamp. ["Discovering an Encyclopaedic Novel: a case study in automatically analysing Harry Mulisch’s The Discovery of Heaven (1992)."](http://www.dhbenelux.org/wp-content/uploads/2016/05/39_Van_Wissen_Van_Erp_Peperkamp_FinalAbstract_DHBenelux2016_short.pdf)

## Usage
* Open `main.py` and point to the correct dependencies (i.e. local version Spotlight, DBpedia Dump and parsed textfile)

## Visualization
[![preview-visualization](https://github.com/LvanWissen/Ontdekking/blob/master/visualization/images/preview.png)](http://kyoto.let.vu.nl/~vanerp/TheDiscoveryOfHeaven/)

See visualization at http://kyoto.let.vu.nl/~vanerp/TheDiscoveryOfHeaven/

## Dependencies
* Named Entity Recognition: [`DBpedia Spotlight`](https://github.com/dbpedia-spotlight/dbpedia-spotlight/wiki/Run-from-a-JAR)
* Visualized by [`InteractiveVis project`] (http://blogs.oii.ox.ac.uk/vis/)
* Python3 packages:
 *   networkx
 *   matplotlib
 *   requests
 *   rdflib
 *   SPARQLWrapper
