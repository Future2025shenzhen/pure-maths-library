import math

def close(actual, expected, tolerance=5e-3):
    assert abs(actual - expected) <= tolerance, (actual, expected)

# Independent recomputation of the non-trivial numerical results used in V14.
a = (math.pi - 2) / 2
side = math.sqrt(4**2 + 5**2 - 40 * math.cos(a))
close(side, 2.709, .001)
close(25 + 40 * math.sin(a) / 2, 35.806, .001)

theta = math.acos(7 / 25)
segment = 50 * (theta - math.sin(theta))
radius2 = 6 / math.sin(theta / 4)
segment2 = radius2**2 / 2 * (theta / 2 - math.sin(theta / 2))
close(theta, 1.287, .001)
close(segment, 16.4, .05)
close(radius2, 19.0, .05)
close(segment2, 7.83, .01)

h = (71.2 - segment) / 12
close(h, 4.57, .01)
close(10 * theta + 12 + 2 * h, 34.0, .05)
close(100 * segment / 71.2, 23.0, .05)

r = math.sqrt((220 / 9) * math.sin(1.2))
bc = math.sqrt(8**2 + 11**2 - 176 * math.cos(1.2))
altitude = 88 * math.sin(1.2) / bc
close(r, 4.77, .01)
close(altitude, 7.45, .01)
close(19 + bc - .8 * r, 26.2, .05)

obtuse = math.pi - math.asin(2 * math.sin(.4))
od = 14 * math.sin(math.pi - obtuse - .4) / math.sin(obtuse)
close(obtuse, 2.249, .001)
close(od, 8.50, .01)

coord_theta = math.atan2(6, 4.5)
close(12.5 * coord_theta, 11.6, .05)
close(.5 * 12.5**2 * coord_theta - 7.5, 64.9, .05)

blade_theta = (2 * math.pi - 1.2) / 6
close(243 * blade_theta, 206, .5)
close(243 * blade_theta + 243 * math.sin(.2), 254, .5)
close(54 * blade_theta + 108 * math.sin(.1), 56.5, .05)

x = 4 * math.sqrt(3)
perimeter = 1.1 * (12 + x) + 2 * (12 - x)
reduction = 1.1 * x - 2 * x * math.sin(.55)
close(perimeter, 31.0, .05)
close(100 * reduction / perimeter, 1.22, .01)
print('PASS V14 independent numerical audit')
