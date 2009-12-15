reductions = {}

base_units = ["kg", "m", "s", "C", "degrees"]

reductions["N"] = {"kg":1, "m": 1, "s":-2}
reductions["J"] = {"kg":1, "m": 2, "s":-2}
reductions["A"] = {                "s":-1, "C": 1}
reductions["F"] = {"kg":1, "m":-2, "s": 2, "C": 2}
reductions["V"] = {"kg":1, "m": 2, "s":-2, "C":-1}

def (reduction, dimensions):
   for dim,unit in reduction:
   
def can_reduce(dimensions):
  for k,v in dimensions:
    for r in reductions:
      if    


class units:
  def __init__(self, value, dimensions=None):
    self.value=value
    self.dimensions= dimensions if dimensions != None else {}

  def __add__(self, other):
    assert self.dimensions == other.dimensions
    return units(self.value + other.value, self.dimensions)

  def __add__(self, other):
    assert self.dimensions == other.dimensions
    return units(self.value + other.value, self.dimensions)

  def __mult__(self, other):
    if not isinstance(other, units):
      assert isinstance(other, (int, long, float, complex))
      return units(self.value * other, self.dimensions)
    new_dimensions = self.dimensions.copy()
    for d,v in other.dimensions.items():
      if d in new_dimensions:
        new_dimensions[d] += v
        if new_dimensions[d] == 0: del new_dimensions[d]
      else:
        new_dimensions[d] = v
    return units(self.value*other.value, new_dimensions)

  def __div__(self, other):
    if not isinstance(other, units):
      assert isinstance(other, (int, long, float, complex))
      return units(self.value / other, self.dimensions)
    new_dimensions = self.dimensions.copy()
    for d,v in other.dimensions.items():
      if d in new_dimensions:
        new_dimensions[d] -= v
        if new_dimensions[d] == 0: del new_dimensions[d]
      else:
        new_dimensions[d] = -v
    return units(self.value/other.value, new_dimensions)
        
  def build_unit_str(self):
    item_to_str = lambda x: str(x[0])+(("^"+str(x[1])) if x[1] != 1 else "")
    return "*".join(map(item_to_str, sorted(self.dimensions.iteritems(), lambda a,b: a[1] < b[1])))

  def __str__(self):
    from si_prefix import si_prefix
    if len(self.dimensions) == 0:
      return str(self.value)
    elif len(self.dimensions) == 1:
      (adjusted_value, prefix) = si_prefix(self.value)
      return str(adjusted_value)+" "+prefix+self.build_unit_str()
    else:
      return str(self.value)+" "+self.build_unit_str()


