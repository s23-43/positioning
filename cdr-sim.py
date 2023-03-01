import sympy as sp
from math import sqrt

# TODO: This works but is slow (~400ms) on my rig. Implement this into positioning.py for now

x,y = sp.symbols("x,y")

#r1, r2, r3 = sqrt(32), sqrt(17), sqrt(37)
r1, r2, r3 = 5.66, 4.12, 6.08 # Approximated (2 sigfigs of sqrt values)

x1, x2, x3 = 0, 3, 10
y1, y2, y3 = 0, 8,  5

f1 = sp.Eq(r1**2, x**2 - 2*x1*x + x1**2 + y**2 - 2*y1*y + y1**2)
f2 = sp.Eq(r2**2, x**2 - 2*x2*x + x2**2 + y**2 - 2*y2*y + y2**2)
f3 = sp.Eq(r3**2, x**2 - 2*x3*x + x3**2 + y**2 - 2*y3*y + y3**2)
print(sp.solve([f1,f2], (x,y)))
print(sp.solve([f1,f3], (x,y)))
print(sp.solve([f2,f3], (x,y)))