#This contains a set of functions for finding alternate possible examples for looking up objects in physnet

#
# Initialization stuff
#
from csc.divisi.util import get_picklecached_thing
from csc.divisi.blend import Blend
from csc.divisi.flavors import ConceptByFeatureMatrix
from csc.conceptnet.models import en
from csc.conceptnet.analogyspace import conceptnet_2d_from_db, make_category
import os

try:
    FILEPATH = os.path.dirname(__file__) or '.'
except NameError:
    FILEPATH = '.'
   

def _make_size_matrix():
    matrixlist = []
    sizefile = open("sizes")
    for line in sizefile:
        l = eval(line)
        matrixlist.append(((l[0],l[1][1],l[1][2]),20))
    return ConceptByFeatureMatrix.from_triples(matrixlist)
    
    
def _get_size_blend():
    sizes = get_picklecached_thing(FILEPATH+os.sep+'sizematrix.pickle.gz', _make_size_matrix)
    cnet = get_picklecached_thing(FILEPATH+os.sep+'cnet.pickle.gz', lambda: conceptnet_2d_from_db('en'))
    size_blend = Blend([sizes, cnet]).normalized(mode=[0,1]).bake()
    return size_blend
    
#sizeblend = get_picklecached_thing(FILEPATH+os.sep+'sizeblend.pickle.gz', _get_size_blend)
#sizesvd = sizeblend.svd(k=100)

#cnet_norm = conceptnet_2d_from_db('en').normalized()
#rawsvd = cnet_norm.svd()

def get_similar_size_examples(concept):
    concept_vector = sizesvd.weighted_u[concept,:].hat()
    like_concepts = sizesvd.u_angles_to(concept_vector)
    return like_concepts    

def get_similar_raw_examples(concept):
    concept_vector = rawsvd.weighted_u[concept,:].hat()
    like_concepts = rawsvd.u_angles_to(concept_vector)
    return like_concepts

def compare_blend(concept):
    print "Raw database:"
    for e in get_similar_raw_examples(concept).top_items():
        print e
    print "Blended database:"
    for e in get_similar_size_examples(concept).top_items():
        print e
#Approach 1: Directly measure similarty in the basic analogy space
