import json

def query_weight(concept):
    db = json.load(file("scraping/db.json"))
    if not concept in db:
        print "%s not found in db." % concept
        return
    concept_db = db[concept]
    if not "weight" in concept_db:
        print "weight not found in db for %s" % concept
    weights = concept_db["weight"]
    return weights  

def get_raw(weights):
    return map(float, weights.keys())
    

def get_average(items):
    return sum(items)/len(items)
        
def get_var(items):
    avg = get_average(items)
    return sum(map(lambda x: (x-average)**2, items))/len(items)
    
def stddv(items):
    return get_var(items)**0.5
    
def filter_outliers(m, stddevs=1.0):
    avg = get_average(m.keys())
    dv = stddv(m.keys())
    minval = avg-dv
    maxval = avg+dv
#    result = reduce new: 
#    return filter(lambda x

def get_wp_entries(query_target):
    wp_db = json.load(file("scraping/db.json"))
    wp_target = query_target.replace(" ", "_")
    if not query_target in wp_db:
        print "%s not found in wikipedia database. Attempting to scrape new version." % query_target
        os.system("perl scraping/wikipedia.pl \"%s\" scraping/db.json" % wp_target)
        wp_db = json.load(file("scraping/db.json"))
        if not wp_target in wp_db:
            print "Unable to find additional data."
            return None
    return wp_db[wp_target]["weight"]

def get_physnet_entries(query_target):
    physnet_db = json.load(file("physnet.json"))
    if not query_target in physnet_db:
        return None
    return physnet_db[query_target]["weight"]

def get_similar_options(query_target):
    print "Looking for alternative queries that might be comparable"
    similar_options = get_similar_size_examples(query_target)
    return similar_options

def invert(d):
    return dict(map(lambda l: (l[1], l[0]), d.iteritems()))

def add_flag(flag, d):
    return dict(map(lambda l: (flag+":"+l[0], l[1]), d.iteritems()))
    
def get_basic_options(query_target):
    print "Looking up basic options for %s" % query_target
    all_data = {}
    
    wp_data = get_wp_entries(query_target)
    #print "Wikipedia data:\n",json.dumps(wp_data, sort_keys=True, indent=4)
    
    if wp_data != None:
        all_data.update(invert(wp_data))
    
    physnet_data = get_physnet_entries(query_target)
    if physnet_data != None:
        all_data.update(invert(physnet_data))

    return all_data

def do_lookup(query_target):
    print "Looking up data for weight of %s" % query_target
    base_data = get_basic_options(query_target)
    
    similar_options = get_similar_options(query_target)
    if similar_options != None:
        print "Looking up additional data in %s" % str(similar_options.top_items())
        for option in similar_options.top_items():
            if option[0] == query_target: continue
            opt_data = get_basic_options(option[0])
            flagged_data = add_flag(("Similar to %s" % str(option)), opt_data)
            #print "Found data on %s:\n" % str(option), json.dumps(flagged_data)
            base_data.update(flagged_data)
        
    print json.dumps(base_data, sort_keys=True, indent=4)

if __name__ == "__main__":
    import sys, os
    from physnet_find_similar import get_similar_size_examples

    if len(sys.argv) > 1:
        query_target = sys.argv[1]
        do_lookup(query_target)
    else:
        while True:
            query_target = raw_input("Enter query [q for quit]:")
            if query_target == "q":
                break
            do_lookup(query_target)
            
            
        
        
        
        
