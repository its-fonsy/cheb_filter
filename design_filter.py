#!/usr/bin/env python3

import math

# commercial value
com_val = [ 1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0,
            2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3,
            4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1 ]
# resistance goes from 100 ohm to 91k ohm
res_exps = [100, 1000, 10e3]
# capacitors goes from 1pF to 9.1nF
cap_exps = [1e-12, 10e-12, 100e-12, 1e-9]


def near_commercial(val):
    """ Function that finds the nearest commercial value
        of capacitance/resistance """

    # determine if the val is a resistor or capacitor
    if int(val) > 0 :
        exps = res_exps
    else:
        exps = cap_exps

    # search the nearest commercial value
    best = 1
    best_diff = 1e9
    for v in [v*e for v in com_val for e in exps]:
        diff = abs(val - v)
        if (diff < best_diff):
            best = v
            best_diff = diff

    return best, (best_diff * 100 / val)


def tow_thomas(w,q):
    """ Find the best component for a Tow-Thomas filter with gain of 1 """

    best_diff = 1e9
    best_c = 1
    best_r = 1
    best_r2 = 1
    exact_r = 1 
    exact_r2 = 1 

    # Find the value of resistance for each capacitor
    # Save the one with nearest value of resistor r and r2
    # to commercial value
    for c in [c*e for c in com_val for e in cap_exps]:
        r = 1 / (w * c)
        near_r, diff1 = near_commercial(r)
        r2 = q * r
        near_r2, diff2 = near_commercial(r2)
        if (diff1 + diff2 ) < best_diff :
            best_c = c 
            best_r2 = near_r2 
            exact_r2 = r2 
            best_r = near_r 
            exact_r = r 
            best_diff = diff1 + diff2
    
    return best_c, exact_r2, best_r2, exact_r, best_r


def sallen_key(w, q):
    """ Find the best component for a Sallen&Key filter with gain of 1 """
    best_diff = 10
    best_c1 = 1
    best_c2 = 1
    best_r = 1

    # Find the value of R and C2 for each C1 in commercial value
    # Save the one with nearest value of C2 to commercial value
    for c in [c*e for c in com_val for e in cap_exps]:
        c2 = c * q**2 * 4
        near_c2, diff = near_commercial(c2)
        r = 1 / (w * math.sqrt(c * c2))
        if diff < best_diff :
            best_c1 = c 
            best_c2 = near_c2 
            exact_c2 = c2
            best_r = r 
            best_diff = diff

    return best_c1, exact_c2, best_c2, best_r


if __name__ == '__main__':
    w = 70384
    q = 2.198018361820587
    print(f"Design fitler with w={w} and Q={q}")
    best_c, exact_r2, best_r2, exact_r, best_r = tow_thomas(w,q)
    print("Thow Thomas")
    print("===========")
    print(f"        C = {best_c} F")
    print(f"  exact R = {int(exact_r)} ohm --> commercial R = {int(best_r)} ohm")
    print(f" exact R2 = {int(exact_r2)} ohm --> commercial R2 = {int(best_r2)} ohm\n")

    c1, c2, best_c2, r = sallen_key(w,q)
    print("Sallen & Key")
    print("============")
    print(f"  C1 = {c1} F")
    print(f"  C2 = {c2} F --> commercial C2 = {best_c2} F")
    print(f"  R = {int(r)} ohm")
