def _default_sign(value):
    if value < 0: return -1
    if value > 0: return 1
    return 0

class interval:
    def __init__(self, min=None, max=None, sign_function=_default_sign):
        assert min==None or max==None or min<=max
        
        self.min = min
        self.max = max
        self._sign = sign_function
        

    def _no_lower_bound(self): return self.min == None
    def _no_upper_bound(self): return self.max == None
    def _has_neg(self): return self.min == None or self._sign(self.min) == -1
    def _has_pos(self): return self.max == None or self._sign(self.max) == 1
    def _pos_and_neg(self): return self._has_neg() and self._has_pos()
    def _two_sided(self): return self.min != None and self.max != None
    def _unbounded(self): return self.min == None and self.max == None
    def _min_zero(self): return self.min != None and self._sign(self.min) == 0
    def _max_zero(self): return self.max != None and self._sign(self.max) == 0
    def _pos_zero(self): return self._pos_and_neg() or self._min_zero() and self._has_pos()
    def _neg_zero(self): return self._pos_and_neg() or self._max_zero() and self._has_neg()
    def _is_zero(self): return self._min_zero() and self._max_zero()
    
    def __add__(self, other):
        no_lower_bound = self._no_lower_bound() or other._no_lower_bound()
        no_upper_bound = self._no_upper_bound() or other._no_upper_bound()
        new_min = None if no_lower_bound else (self.min + other.min)
        new_max = None if no_upper_bound else (self.max + other.max)
        
        assert new_min == None or new_max == None or new_min <= new_max 
        
        return interval(new_min, new_max)
        
    def __sub__(self, other):
        no_lower_bound = self._no_lower_bound() or other._no_upper_bound()
        no_upper_bound = self._no_upper_bound() or other._no_lower_bound()
        new_min = None if no_lower_bound else (self.min - other.max)
        new_max = None if no_upper_bound else (self.max - other.min)

        assert new_min == None or new_max == None or new_min <= new_max 
        
        return interval(new_min, new_max)
        
    def __mul__(self, other):
        no_lower_bound = \
            ( self._no_upper_bound() and other._has_neg()) or \
            ( self._no_lower_bound() and other._has_pos()) or \
            (other._no_upper_bound() and  self._has_neg()) or \
            (other._no_lower_bound() and  self._has_pos())
            
        no_upper_bound = \
            ( self._no_upper_bound() and other._has_pos()) or \
            ( self._no_lower_bound() and other._has_neg()) or \
            (other._no_upper_bound() and  self._has_pos()) or \
            (other._no_lower_bound() and  self._has_neg())

        options = []
        if self.min != None and other.min != None: options.append(self.min * other.min)
        if self.min != None and other.max != None: options.append(self.min * other.max)
        if self.max != None and other.min != None: options.append(self.max * other.min)
        if self.max != None and other.max != None: options.append(self.max * other.max)
        
        #TODO worry about [0,0]*[-inf,inf] which will create an error here
        #TODO worry about [0,0]*[a,inf] which will return [0,0]
        
        new_min = None if no_lower_bound else min(options)
        new_max = None if no_upper_bound else max(options)
        
        assert new_min == None or new_max == None or new_min <= new_max 
        
        return interval(new_min, new_max)
    
    

    def __div__(self, other):
        no_lower_bound = \
            ( self._pos_zero() and other._has_neg()) or \
            (other._pos_zero() and  self._has_neg()) or \
            ( self._neg_zero() and other._has_pos()) or \
            (other._neg_zero() and  self._has_pos()) or \
            ( self._is_zero() and other._has_neg()) or \
            (other._is_zero() and  self._has_neg())
            
        no_upper_bound = \
            ( self._pos_zero() and other._has_pos()) or \
            (other._pos_zero() and  self._has_pos()) or \
            ( self._neg_zero() and other._has_neg()) or \
            (other._neg_zero() and  self._has_neg()) or \
            ( self._is_zero() and other._has_pos()) or \
            (other._is_zero() and  self._has_pos())
            
        assert not (self._is_zero() and other._is_zero())
        
        options = []
        if self.min != None and other.min != None: options.append(self.min / other.min)
        if self.min != None and other.max != None: options.append(self.min / other.max)
        if self.max != None and other.min != None: options.append(self.max / other.min)
        if self.max != None and other.max != None: options.append(self.max / other.max)
        
        new_min = None if no_lower_bound else min(options)
        new_max = None if no_upper_bound else max(options)
        
        assert new_min == None or new_max == None or new_min <= new_max 
        
        return interval(new_min, new_max)

    def __contains__(self, item):
        return \
            (self._no_lower_bound() or item > self.min) and \
            (self._no_upper_bound() or item < self.max)

    def __repr__(self):
        return "interval(%s, %s)" % (self.min, self.max)
    def __str__(self):
        if self._two_sided():
            return "[%s to %s]" % (str(self.min), str(self.max))
        elif self._unbounded():
            return "<unbounded range>"
        elif self._no_upper_bound():
            return "X>=%s" % str(self.min)
        elif self._no_lower_bound():
            return "X<=%s" % str(self.max)
        else:
            assert False
        
        
        
        
        
        