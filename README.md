# Low pass Chebyshev filter
Python script to implement a low pass Chebyshev filter with Tow-Thomas or
Sallen & Key circuit.

## Install and usage
With `python3` already installed

	git clone https://github.com/its-fonsy/cheb_filter.git
	cd cheb_filter

To work correctly the script need `Amax Amin fp fs G` (in this order) as
parameter when lunch. So an example of correct use would be

	python -B cheb.py 1 20 15000 20000 5

the `-B` flag is for preventing python to generate the folder `__pycache__`.

## Example of output
An example of the output would be

```
  Specs
  =====
  Amax = 1
  Amin = 20
  fp = 15000
  fp = 20000
  G = 5

  Calculate the order of the filter
  ===================================
  ε=0.5088471399095875

  Find the minimum order
    with N = 2 --> A is 3.6151629991213756
    with N = 3 --> A is 7.837518586503201
    with N = 4 --> A is 13.449096456182193
    with N = 5 --> A is 19.553801351470202
    with N = 6 --> A is 25.7896385433968
  The filter will be of order 6

  Calculate the poles
  =====================
  p1 = wp(-0.06218102379301138+0.993411202482326j)
  p2 = wp(-0.16988171626915632+0.7272274730251562j)
  p3 = wp(-0.23206274006216773+0.2661837294571697j)
  p4 = wp(-0.23206274006216773-0.26618372945716984j)
  p5 = wp(-0.16988171626915635-0.7272274730251561j)
  p6 = wp(-0.06218102379301145-0.9934112024823258j)

  Transfer Function
  =================
                                              5 ⍵p^6
  ----------------------------------------------------------------------------------------
  16.2831(s² + s‧⍵p‧0.1244 + 0.9907)(s² + s‧⍵p‧0.3398 + 0.5577)(s² + s‧⍵p‧0.4641 + 0.1247)

  Calculate w and Q for filters
  =============================
  w = 93810 with a Q = 8.0037
  w = 70384 with a Q = 2.1980
  w = 33282 with a Q = 0.7609

  Sallen and Key filters
  ======================
  For w=93810 and Q=8.00
    C1 = 3.9e-12 F
     R = 170752 ohm
    C2 = 9.993214080813776e-10 F --> commercial C2 = 1e-09 F

  For w=70384 and Q=2.20
    C1 = 6.2e-12 F
     R = 521276 ohm
    C2 = 1.1981586102873136e-10 F --> commercial C2 = 1.2e-10 F

  For w=33282 and Q=0.76
    C1 = 2.2000000000000003e-12 F
     R = 8974724 ohm
    C2 = 5.0945087072459805e-12 F --> commercial C2 = 5.1e-12 F

  Tow-Thomas filters
  ==================
  For w=93810 and Q=8.00
     C = 3.9e-09 F
     R = 2733 ohm -> commercial R = 2700 ohm
    R2 = 21876 ohm -> commercial R2 = 22000 ohm

  For w=70384 and Q=2.20
     C = 1.3e-09 F
     R = 10928 ohm -> commercial R = 11000 ohm
    R2 = 24021 ohm -> commercial R2 = 24000 ohm

  For w=33282 and Q=0.76
     C = 1.5000000000000002e-09 F
     R = 20030 ohm -> commercial R = 20000 ohm
    R2 = 15240 ohm -> commercial R2 = 15000 ohm

  Resistance to set the G
  =======================
  Opamp in inverting amplifier configuration
  R1 = 10000 ohm
  R2 = 50000 ohm
```

## Components for Sallen-Key filter
Using the *smart* strategy when designing the filter the algorithm try to use
two capacitance of commercial value. The resistor is calculated from those
value.


## Components for Tow-Thomas filter
The algorithm calculate all the value of both resistance for each commercial
capacitor. Then it display the one with nearest value, for both resistance, the
commercial one.


## Circuits reference 
TO BE DONE
