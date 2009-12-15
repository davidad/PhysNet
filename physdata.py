# want to be able to enter "1.23 mV" and get units(range(1.225e-3,1.235e-3), {"kg":1, "m": 2, "s":-2, "C":-1})

reductions = {}
reductions["N"] = (3,{"g":1, "m": 1, "s":-2})
reductions["J"] = (3,{"g":1, "m": 2, "s":-2})
reductions["A"] = (0,{               "s":-1, "C": 1})
reductions["F"] = (3,{"g":1, "m":-2, "s": 2, "C": 2})
reductions["V"] = (3,{"g":1, "m": 2, "s":-2, "C":-1})


def map_add(first, second, exp):
    for k in second:
        if not k in first: first[k] = 0
        first[k] += second[k]*exp
            
def update_unit(unit_map, unit_str, sign):
    #print "update unit for %s" % unit_str
    split = unit_str.split("^")
    #print "split to %s" % str(split)
    prefixes = {'y':-24,'z':-21,'a':-18,'f':-15,'p':-12,'n':-9,'u':-6,'m':-3,'c':-2,'':0,'k':3,'M':6,'G':9,'T':12,'P':15,'E':18,'Z':21,'Y':24}
    
    unit_exponent = 1 #exponent for the number of times the unit is repeated
    if len(split) > 1: unit_exponent = int(split[1])
    #print "Unit exponent = %d" % unit_exponent
    
    
    prefix = split[0][0:-1]
    unit = split[0][-1:]
    
    num_exponent = sign*prefixes[prefix]*unit_exponent
    #print "numerical exponent based on prefix = %s and unit = %s: %d" % (prefix, unit, num_exponent)
    
    if unit in reductions:
        map_add(unit_map, reductions[unit][1], sign*unit_exponent)
        num_exponent += sign*reductions[unit][0]*unit_exponent
    else:
        if not unit in unit_map: unit_map[unit] = 0
        unit_map[unit] += sign*unit_exponent
            
    return num_exponent

from interval import interval
from units import units
        
def phys(string):
    string = string.strip()
    mantissa_str = None
    exponent_str = None
    numerical_str = None
    unit_str = None
    first_sig_fig = -1
    last_sig_fig = -1
    exponent_start = -1
    decimal_position = -1
    for i, c in enumerate(string):
        
        #find the part that contains the number and pull out sigfigs and exponent location
        if c not in "-+0123456789eE." or i == len(string)-1:
            #check if the e was supposed to be part of the units
            if exponent_start == -1: exponent_start = i
            mantissa_str = string[0:exponent_start].strip()
            exponent_str = string[exponent_start:i].strip()
            numerical_str = string[0:i].strip()
            unit_str = string[i:].strip()
            break #we are done here so move on to conversions
            
        #look for the exponent
        if c in "eE":
            assert exponent_start == -1 #only one exponent allowed
            exponent_start = i
        
        #look for the decimal
        if c in ".":
            assert decimal_position == -1 #only one decimal allowed
            decimal_position = i
        
        #look for sigfigs
        if c in "123456789" and exponent_start == -1:
            if first_sig_fig == -1: first_sig_fig = i
            last_sig_fig = i
        elif c == "0" and decimal_position != -1:
            last_sig_fig = 
        
            #print "Last sig fig now", c

    if decimal_position == -1: decimal_position = len(mantissa_str)
    
    base = float(mantissa_str)
    exponent = 0 if len(exponent_str) <= 1 else int(exponent_str[1:]) #trim off the 'e' if it is there
                
    #we want to know the rounding error which will be 0.5 times the exponent of the last significant figure
    last_sigfig_exponent = None
    sigfigs = None
    
    #make sure we have at least one
    if first_sig_fig != -1:

        #no need to take care of a minus sign or such because that can't be in the middle and still have a valid number

        #adjust for the decimal place if it was in the middle
        if first_sig_fig <= decimal_position and decimal_position <= last_sig_fig:
            #print "in middle"
            last_sigfig_exponent = decimal_position-last_sig_fig+exponent
            sigfigs = last_sig_fig - first_sig_fig
        else:
            #print "not in middle"
            last_sigfig_exponent = decimal_position-last_sig_fig+exponent-1
            sigfigs = 1 + last_sig_fig - first_sig_fig
        
    
    unit_str = unit_str.replace(" ","")
    unit_list = unit_str.split("/")
    if "" in unit_list: unit_list.remove("")
    assert len(unit_list) <= 2 #make sure there was only one "/"
    pos_units = unit_list[0].split("*") if len(unit_list) >= 1 else []
    neg_units = unit_list[1].split("*") if len(unit_list) >= 2 else []
    
    unit_map = {}
    unit_exponent_delta = 0
    for u in pos_units: unit_exponent_delta += update_unit(unit_map, u, 1)
    for u in neg_units: unit_exponent_delta += update_unit(unit_map, u, -1)
    
    exponent += unit_exponent_delta
    last_sigfig_exponent += unit_exponent_delta
    
    #print "base = %f" % float(mantissa_str)
    #print "exponent = %d" % exponent
    #print "sigfigs = %d" % sigfigs
    #print "error = 0.5*10**%d" % last_sigfig_exponent
    #print "pos units = %s" % str(pos_units)
    #print "neg units = %s" % str(neg_units)
    #print "unit map = %s" % str(unit_map)
    
    num_val = float(numerical_str)*10**unit_exponent_delta
    error = 0.5*10**last_sigfig_exponent
    return units(interval(num_val-error,num_val+error), unit_map)

#phys("1.23mm")
#print
#phys("1.23E3 km")
#print phys("-123. mm^-3")
#print
#print phys("-10.0 km")

    
