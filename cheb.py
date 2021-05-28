#/usr/bin/env python3

import math
from prettytable import PrettyTable
import design_filter

# Specs
A_max = 1
A_min = 20

fp = 15e3
fs = 20e3

G = 5

# print specs
print("\n  Specs")
print("  =====")
spec_table = PrettyTable(["Amax", "Amin", "fp", "fs", "G"])
spec_table.add_row([A_max, A_min, fp, fs, G])
print(spec_table)

print("\n  Calculate the order of the filter")
print("  ===================================")
epsilon = math.sqrt(10**(A_max/10) - 1)
print(f"  ε={epsilon}\n")

# establish the order of the filter
print("  Find the minimum order")
N = 1
A = 10 * math.log(1 + epsilon**2 * math.cosh(N * math.acos(fp / fs))**2)
while(A < A_min):
    N += 1
    A = 10 * math.log10(1 + epsilon**2 * math.cosh(N * math.acos(fp / fs))**2)
    print(f"    with N = {N} --> A is {A}")
print(f"  The filter will be of order {N}\n")

# calculate the poles
print("  Calculate the poles")
print("  =====================")
poles = []
for k in range(1, N+1):
    p_real = -math.sin( (2 * k - 1)/N * math.pi/2 ) * math.sinh(1/N * math.asinh(1/epsilon))
    p_im = math.cos( (2 * k - 1)/N * math.pi/2 ) * math.cosh(1/N * math.asinh(1/epsilon))
    p = complex(p_real, p_im)
    poles.append(p)
    print(f"  p{k} = wp{p}")

print("\n  Transfer Function")
print("  =================")

tf_poles = []


# print the ratio line of the right dimension
# fixed 27 chars to write a second order pole
# fixed 15 chars to write a first order pole
# fixed 7 chars to write epsilon*2^(N-1)
if N % 2:
    ratio_len = 27 * int(N/2) + 15 + 7
else:
    ratio_len = 27 * int(N/2) + 7

print('  ' + ' '*int(ratio_len/2) + f"{G} ⍵p^{N}")
print('  ' + '-'*ratio_len)

eps_two_power_N_min_one = epsilon * 2**(N-1) 
print(f"  {format(eps_two_power_N_min_one,'.4f')}", end='')

# in case of odd order filters
if ( N % 2 ):
    order_one_pole = -poles[int(N/2)].real
    tf_poles.append([0, order_one_pole])
    print(f"(s + ⍵p‧{format(order_one_pole, '.4f')})", end='')

# then calculate all the second order poles
for t in range(int(N/2)):
    b = poles[t].real + poles[N-t-1].real
    c = poles[t] * poles[N-t-1]
    tf_poles.append([-b, c.real])
    print(f"(s² + s‧⍵p‧{format(-b, '.4f')} + {format(c.real, '.4f')})", end='')

print("\n\n  Calculate w and Q for filters")
print("  =============================")

filter_specs = []
for pole in tf_poles:
    if pole[0] == 0:
        # first order pole
        w = 2 * math.pi * fp * pole[1]
        filter_specs.append([w, 0])
    else:
        # second order pole
        w = 2 * math.pi * fp * math.sqrt(pole[1])
        Q = w / (pole[0] * 2 * math.pi * fp)
        filter_specs.append([w, Q])

filt_table = PrettyTable(["w [rad/s]", "Q"])
for spec in filter_specs:
    filt_table.add_row([int(spec[0]), spec[1]])
filt_table.sortby = "Q"
print(filt_table)

print("\n  Sallen and Key filters")
print("  ======================")

for spec in filter_specs:
    w, q = spec
    if q != 0:
        c1, exact_c2, near_c2, r = design_filter.sallen_key(w,q)
        print(f"  For w={int(w)} and Q={format(q, '.2f')}")
        print(f"    C1 = {c1} F")
        print(f"     R = {int(r)} ohm")
        print(f"    C2 = {exact_c2} F --> commercial C2 = {near_c2} F\n")


print("  Tow-Thomas filters")
print("  ==================")

for spec in filter_specs:
    w, q = spec
    if q != 0:
        c, exact_r2, near_r2, exact_r, near_r = design_filter.tow_thomas(w,q)
        print(f"  For w={int(w)} and Q={format(q, '.2f')}")
        print(f"     C = {c} F")
        print(f"     R = {int(exact_r)} ohm -> commercial R = {int(near_r)} ohm")
        print(f"    R2 = {int(exact_r2)} ohm -> commercial R2 = {int(near_r2)} ohm\n")


if N % 2:
    print("  First order filters")
    print("  ===================")

    for spec in filter_specs:
        w, q = spec
        if q == 0:
            c = 1e-9
            r2 = 1 / (w * c)
            r1 = r2 / G
            print(f"  For w={int(w)}")
            print(f"     C = {c} F")
            print(f"    R1 = {int(r1)} ohm")
            print(f"    R2 = {int(r2)} ohm\n")
