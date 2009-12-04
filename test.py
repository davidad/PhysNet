from hypothesis import *
from interval import interval

weight_of_an_elephant = log_set()
weight_of_an_elephant.add_new(["David"], interval(26, 26))
weight_of_an_elephant.add_new(["Forrest"], interval(10,11))
weight_of_an_elephant.add_new(["Default"], interval(0,None))

print "Weight of an elephant:"
weight_of_an_elephant._print()


number_of_elephants_in_africa = log_set()
number_of_elephants_in_africa.add_new(["Forrest"], interval(10, 10))
number_of_elephants_in_africa.add_new(["David"], interval(10, 69))

print "Number of elephants:"
number_of_elephants_in_africa._print()

number_of_elephants_in_new_york = log_set()
number_of_elephants_in_new_york.add_new(["Forrest"], interval(9, 12))
number_of_elephants_in_new_york.add_new(["David"], interval(2, 5))

elephant_mass_africa = weight_of_an_elephant * number_of_elephants_in_africa
justify(elephant_mass_africa, "I wanted elephants in africa")

elephant_mass_new_york = weight_of_an_elephant * number_of_elephants_in_new_york
justify(elephant_mass_new_york, "I care about elephants in new_york")
print "New york elephant mass:"
elephant_mass_new_york._print()



all_elephants = weight_of_an_elephant * either(number_of_elephants_in_africa, number_of_elephants_in_new_york)
justify(all_elephants, "I care about all of them")

print "all_elephants:"
all_elephants._print()



all_elephants = elephant_mass_new_york + elephant_mass_africa
justify(all_elephants, "I care about all of them")

elephant_mass = either(elephant_mass_africa, elephant_mass_new_york, all_elephants)

print "Total elephant mass:"
elephant_mass._print()
