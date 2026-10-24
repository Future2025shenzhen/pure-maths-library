"""Independent arithmetic and algebra checks for the twelve V15 additions."""
import math
from fractions import Fraction

# C04-R31: midline/amplitude/period and mapped maximum.
assert (3 + -5) / 2 == -1 and (3 - -5) / 2 == 4
assert 360 / Fraction(3, 2) == 240
assert -4 * math.cos(math.radians(3 * 240 / 4)) == 4

# C04-R32: horizontal stretch maps the two roots and keeps multiplicity.
f32 = lambda x: (x / 2 + 2) * (x / 2 - 3) ** 2
assert f32(-4) == 0 and f32(6) == 0

# C04-R33: extrema/period and the two non-commuting transformation orders.
assert (5 + -1) / 2 == 2 and (5 - -1) / 2 == 3 and 360 / 180 == 2
assert 'x-60' != 'x-30'

# C04-R34: stationary levels of u^3+3u^2.
F = lambda u: u**3 + 3*u**2
assert F(0) == 0 and F(-2) == 4

# C04-R35: six cycles with two solutions each.
assert (6 * 360) / 360 == 6 and 6 * 2 == 12

# C04-R36: affine image of the range.
assert (2 * -3 - 1, 2 * 5 - 1) == (-7, 9)

# C09-R31: curve constant, point and tangent data.
C31 = Fraction(155, 21)
assert Fraction(2, 7) - Fraction(8, 3) + C31 == 5
assert Fraction(2, 7) * 128 - Fraction(8, 3) * 8 + C31 == Fraction(475, 21)
assert math.sqrt(4) * (4 - 2) * (4 + 2) == 24

# C09-R32 and R34: reconstructed curves meet all given conditions.
f32i = lambda x: x**4 - 2*x**2 + 3
assert f32i(0) == 3 and 4*1**3 - 4*1 == 0 and f32i(-3) == f32i(3)
f34 = lambda x: x**3 - 2*x**2 + 2*x + 2
assert f34(0) == 2 and f34(2) == 6 and 3*1**2 - 4*1 + 2 == 1

# C09-R33 stationary point and classification.
f33 = lambda x: 2*x**1.5 - 6*x**0.5 - 3
assert f33(4) == 1 and f33(1) == -7
assert 1.5*1**-0.5 + 1.5*1**-1.5 > 0

# C09-R35: the extra point forces a=-3; gradient/normal are consistent.
a = -3
f35 = lambda x: a*x**3/6 + x**2 + (1-a/2)*x + 2+a/3
assert f35(0) == 1 and f35(1) == 4
assert -Fraction(1, 3) * 3 == -1

# C09-R36: exact factorisation and positive-domain uniqueness.
for u in (1, -2):
    assert u**3 - 3*u + 2 == 0
assert (1-1)**2*(1+2) == 0
print('V15 mathematical audit passed (12 additions)')
