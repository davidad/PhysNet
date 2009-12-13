from getch import getch
import sys, random

outfile = open("sizes","a")

def get_answears(prompts):
    results = []
    while len(prompts) > 0:
        p = prompts.pop(random.randrange(len(prompts)))
        obj1 = p[0]
        obj2 = p[1][2]
        sys.stdout.write("\"%s\" \"%s\"" % (obj1, obj2))
        while True:
            response = getch()
            if response == 'z':
                sys.stdout.write("  same\n")
                outfile.write("%s \n" % str(p))
                break
            elif response == 'm':
                sys.stdout.write("  different\n")
                break
            elif response == 'q':
                return

from csc.conceptnet4.analogyspace import conceptnet_2d_from_db
cnet = conceptnet_2d_from_db('en')

similar_size_relations = filter(lambda k: k[1][1] == "SimilarSize", cnet)

print "Similar size relations:"
print similar_size_relations[0:10]

print "'z' for same, 'm' for different"

get_answears(similar_size_relations)
#
#tests = ["test1", "test2", "test3"]
#
#results = get_answears(tests)
#
#print results
