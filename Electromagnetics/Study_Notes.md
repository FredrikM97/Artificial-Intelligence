---
title: Study Notes
---
## What to learn
#### Polar form
* $a + bj$ -> $ \sqrt(a^2+b^2)*\arctan(b/a)$ 
#### Rectangular form
$aL^b$ -> $a*\cos(b) + j\sin(b) = a+bj$
#### Node voltage (Super position)

#### Current divider / Voltage dividor
$R1/R_{tot} * I = I_{divided}$
$R1/R_{tot} * V = V_{divided}$


#### Thevenin voltage, impedence

Voltage: 
* The thevenin voltage is the open circuit voltage at terminals A and B.

Tips: 
* Voltage division until open circuit A and B
* Find $R_{th}

Impedence:

* The Thevenin impedance Z is the impedance seen at AB with all voltage sources replaced by short circuits and all current sources replaced by open circuits

Tips:
* Sum all resistors

#### Norton current
Relationship between THevenin equivalent and Norton equivalent current
$R_{Th} = R_{No}$
$V_{Th} = I_{No}*R_{No}$
$I_{No} = V_{Th}/R_{Th}$

#### Transfer function
Lowpass filter:
$H(f) = V_{out}/V_{in} = (1/jwc)/(R+1/jwc)$ 
Were $w = 2\pi f$
$V_{out} = V_{in}*R/R_{tot}$ (Might be wrong)

According to book:

Formulas:
1) $V_{out} = H(f)*V_{in}$
2) $f_B = 1/(2\pi RC)$ [Hz]
3) $f = w/2\pi$
4) $H(f) = 1/(1 + j(f/f_B))$

Example:
1) Input: $V_{in} = 10cos(250\pi t) + 10cos(500\pi t)$
2) $V_{in1} = 10cos(250\pi t)$
3) $f = 250\pi/2\pi = 125$
4) $H(f) = 1/(1+j(f/f_B)) = 1/(1 + j(125/125)) = 0,0025L^{-45}$
5) $V_{out1} = H(125) * V_{in} = 0,0025L^{-45} * 10L^{0} = 0,024*L^{-45}$
6) Repeat step 1-5 with $V_{in2}$
7)  $V_{out} = H(125) * V_{in1} + H(250)*V_{in2}$

Part 7 may look something like.. $V_{out}(t) = 0,024cos(250\pi t - 45) + H(250)*V_{in2}$

In decibel:
$|H(f)|_{dB} = 20log|H(f)|$
In phase:
$L^{H(f)} = -arctan(f/f_B)$
#### Phasors
Lower grade means it will be after a phasor with higher grade
## Cascade Amplifier
# Sources
http://hyperphysics.phy-astr.gsu.edu/hbase/electric/acthev.html
https://en.wikipedia.org/wiki/Th%C3%A9venin%27s_theorem
https://en.wikipedia.org/wiki/Nodal_analysis
