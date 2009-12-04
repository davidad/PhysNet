
class log:
    def __init__(self, value=None, reasons=None):
        self.raw_value = value
        self.reasons = set()
        if reasons != None: self.reasons.update(reasons)
        self.child = None
        
    def apply(self, operator, operator_str, other):
        new_value = log(operator(self.raw_value, other.raw_value))
        new_value.set_child(operator_str, self, other)
        return new_value
        
    def set_child(self, operator_str, a, b):
        self.child = (operator_str, a, b)
    
    def justify(self, reason):
        self.reasons.add(reason)
    
class log_set:
    def __init__(self):
        self.data = set()
    
    def add_new(self, reasons, value):
        new_log = log(value=value,reasons=reasons)
        self.data.add(new_log)
    
    def __add__(self, other): return apply_log_set(lambda a, b: a+b, "+", self, other)
    def __mul__(self, other): return apply_log_set(lambda a, b: a*b, "*", self, other)


    def _print(self):
        for h in self.data: print "\t%s: %s" % (h.raw_value, ugly_str(h))
        
def ugly_str(log):
    if log.child == None:
        return "%s because %s" % (log.raw_value, log.reasons)
    else:
        return "(%s) %s (%s)%s" % ( \
            ugly_str(log.child[1]),
            log.child[0],
            ugly_str(log.child[2]),
            "" if len(log.reasons) == 0 else " because " + str(log.reasons))
    
        
def apply_log_set(f, fstr, ls1, ls2):
    ns = log_set()
    
    for l1 in ls1.data:
        for l2 in ls2.data:
            new_log = l1.apply(f,fstr,l2)
            ns.data.add(new_log)
            
    return ns
            
def justify(ls, reason):
    for l in ls.data:
        l.justify(reason)
   
def either(*log_sets):
    ns = log_set()
    for ls in log_sets:
        ns.data.update(ls.data)
    return ns


    
class hypothesis:
    def __init__(self, justifications, data=None):
        self.justifications = set()
        self.justifications.update(justifications)            
        self.data = data
    def __repr__(self):
        return "hypothesis(%s, %s)" % (self.justifications, self.data)
    def __str__(self):
        return "%s (based on %s)"  % (str(self.data), str(self.justifications))

def _apply_to_sets(f, s1, s2):
    new_set = hypothesis_set()
    
    for h1 in s1.hypotheses:
        for h2 in s2.hypotheses:
            new_justifications = h1.justifications.union(h2.justifications)
            new_data = f(h1.data, h2.data)
            new_set.add(hypothesis(new_justifications, new_data))

    return new_set
    
class hypothesis_set:
    def __init__(self):
        self.hypotheses = set()

    def add_new(self, justification, data):
        self.add(hypothesis(justification, data))
        
    def add(self, hypothesis):
        self.hypotheses.add(hypothesis)
    
    def operate(self, operator, other): return _apply_to_sets(operator, self, other)
    def __add__(self, other): return _apply_to_sets(lambda a, b: a+b, self, other)
    def __sub__(self, other): return _apply_to_sets(lambda a, b: a-b, self, other)
    def __mul__(self, other): return _apply_to_sets(lambda a, b: a*b, self, other)
    def __div__(self, other): return _apply_to_sets(lambda a, b: a/b, self, other)
    def __pow__(self, other): return _apply_to_sets(lambda a, b: a**b, self, other)

    def _print(self):
        for h in self.hypotheses: print "\t%s" % h
        
        
 #find contradictions
 #condense
 #apply operator
 #merge
 
    
    