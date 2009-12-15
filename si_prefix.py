def si_prefix(value):
  #standard si prefixes
  prefixes = ['y','z','a','f','p','n','u','m','','k','M','G','T','P','E','Z','Y']

  from math import log
  #closest 1000 exponent
  if value == 0: return (value, "")
  exp = int(log(value,1000)//1) + 8
  if exp < 0: exp = 0
  if exp > 16: exp = 16
  return (value*1000**(-(exp-8)), prefixes[exp])


