import newtonian as nt
from newtonian.units import *
from numpy import array
from math import pi as π

n = 3
r = 3
the = 2*π / n

p = nt.Vec.P(r, π/2)
p2 = nt.Vec.P(r, π/2 + the)
p3 = nt.Vec.P(r, π/2 + 2*the)

l = [p, p2, p3] * m
print(l)
l = [_p / m for _p in l]
print(l)
print(*((pos.x, -pos.y) for pos in l))
