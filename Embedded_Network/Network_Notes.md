# Closed Network
* Clos network specified by ($IN, N_1, N_2, N_3, OUT$)
## Condition for clos network to be (strictly) non-blocking 
* $N_2 \geq IN + OUT - 1$
* This is necessary if $N_1 \geq OUT and N_3 \geq IN$
## Condition for a Clos network to be rearrangeably nonblocking
* $N_2 \geq max(IN, OUT)$

# Lecture 4
* Optical Interconnections and networks
* WAN
* Data communication and telecommunication equipment

# Lecture 5
* Embedded System
* Real-time system
## Global cellular Network
- 1G, 2G, 3G, 4G
- Doppler spread caused by movement
- Noise
## Electromagnetic signal
 Function of time (also be expected as a function of frequency)

## Time-domain concepts
- Analog signal, Digital signal, periodic signal
- Aperiodic signal, peak amplitude
- 1G, 2G, 3G, 4G
- Doppler spread caused by movement
- Noise
## Electromagnetic signal
- Function of time (also be expected as a function of frequency)

## Relationship - Data rate and brandwidth
- Greater bandwidth -> higher information carry capacity
- Digital waveform: Infinity bandwidth, transmission system limit bandwidth
- Greater bandwidth, greater cost
 
## Channel capacity
 - Noise, limit data rate
 - C, maximum data rate that can be transmitted over communication path/Channel

## Nyquist bandwidth
 - Maximum data rate of a transmission system
 - B: bandwidth
 - M: Signal level
 - $C = 2B\log_2M$
  
## Signal to noise Ratio (SNR, S/N)
- Typically messured at receiver, Higher SNR, better quality, low need repeaters
- $(SNR)_{dB} = 10\log_{10}(signal power/noise power)$

## Shannon Capacity Formula
- Theoretical maximum that can be achieved (other parameters not incuded in real life system such as white noise)
- $C = B\log_2(1+SNR)$

## General frequency ranges
- Microwave: 1 GHz - 40GHz 
- Radio frequency: 30 MHz - 1 GHz
- Infrared 0.3 THz - 0.2 PHz

## Multiplexing
- Higher data rate -> more cost effective
- Multiple signals on single medium
- Frequency-division multiplexing (FDM)
- Time-devision multiplexing (TDM)

# Lecture 6
## Switching Terms
* Switching nodes (no concern of data content), stations (connected with switching node, "client")
* Communication network (collection of switching nodes)

## Techniques in switched networks
- Circuit switching: Dedicated communication between two stations, public switched telephone network
- Packet switching: Message broken into series of packets

## Circuit switching
- End to end circuit though switching nodes
- Data: Analog digital or binary
- Deallocation of dedicated resources
- Not 100¤ utilization, Network dedicated to user on establish

## Telecommuncation network
- Subscribers (devices attacked to network)
- Subscriber line (between subscriber and network)
- End office: Switching center
- Trunks: branches between exchanges

## Package switching
- Data transmitted in blocks (package), broken into series of packages
- redirected in nodes
- Better efficiency, multiple packages can share same node
- Data-rate conversations, two stations with different data-rate can exchange information

- Packages treated independently
### Advantages
- Increased delivery diplay on heavy traffic but still accept new packages
## Disadvantage
- Delay can be huge with many packages, package require overhead information, destination and sequencing info
- More processing at each node

## Package switching network - Datagram
- Packages treated independetly
- Exit/end node restores package order, loss of package and how to recover
- Datagram: More flexible and reliable

## Package switching network - Virtual circuit
- Route established before package sent
- Packets buffered at each node
- Arrives in same order
- No decisions made at each node

## Effect of Packet Size on Transmission
- Break down packages -> decrease transmission time due to overlap, too small is increases time

## Antenna
- Radiates electromagnetic energy 

## Radiation Patterns
- Beam width
- Radiation/Reception pattern
- Sidelobes
- Nulls
## Types of antennas
- Isotropic, Dipole, parabolic (microwave, satellite), reflective, Directional antenna

## Antenna Gain
- $G = (4\pi A_e)/(\lambda^2) = 4\pi f^2A_e/c²$
G: Antenna gain
$A_e:$ Effective area
$f:$ Carrier frequency
c = speed of light (3*10^8 m/s)
$\lambda:$ carrier wavelength

## Propagation Modes
- Ground-wave (contour to earth), Sky-wave (reflected from ionized layer of atmosphere), Line-of-sight

## Line-of-sight equation
Optical line of sight
* $d = 3.57\sqrt{h}$
Effective, or radio, line of sight
* $d = 3.57\sqrt{Kh}$
Maximum distance between two antennas
* $3.57(\sqrt{Kh_1} + \sqrt{Kh_2})$
$h_1:$ Hight of first antenna
$h_2:$ Hight of second antenna

d: distance between antenna and horizin (km)
h: antenna hight (m)
K: Adjustment factor to account for refraction, K=4/3

## Five basic propagation mechanisms
- Free space propagation, transmission (though medium), Reflection, Diffraction (secondary wave behind object, sharp edge), Scattering (interaction small object or rough surface)

## LoS Wireless - Transmission weakening
- Free space loss, Noise, atmospheric absorption, multipath, refraction

### Attenuation
- Signal, higher level to avoid noise
- Attentuation greater at higher frequencies

# Lecture 7
## Free space loss
$FSPL = (4\pid/\lambda)^2$

With directive antennas:
- P_t/P_r = (4\pid)²/\lambda²G_1G_2 = (4\pifd)^2/C²G_1G_2
$P_t:$ Signal power at transmitted
$P_r:$ Signal power at received
$\lambda:$ carrier wavelength (m)
d: distance between antennas (m)
c: speed of light (3*10⁸ m/s)
$G_1$ and $G_2$: Antenna gains

Isotropic antennas:
$L_{dB} = 10log(P_t/P_r) = 20log(4\pid/\lambda) = -20log(\lambda) + 20log(d) + 21.98 dB = 20log(4\pifd/c) = 20log(f) + 20log(d) - 147.56dB$

## Path Loss Exponent in practical systems
- Reflection, scattering etc..
- Received power decreases logarithmic with distance

- P_t/P_r = (4\pi/\lambda)²d = (4\pif/c)²d^n

## Effect of multipath propagation
- Copies may arrive at different phases

## Fading
- Path loss, doppler spread (time domain), multi-path fading (frequency domain)
- Doppler: Fluctuation caused by movements
- Multi-path: Multiple signals arrive at receiver

* Slow fading: Little noise ($T_c remains almost "unchanged" $, $T_c >> T_b$)
* Fast fading: Much noise and $T_c$ change a lot.

* Flat fading: $B_c >> B_s$, signal fits within bandwidth
* Selective fading: Otherwise it doesnt and some of the signal may be cut out.
# Lecture 8
## Things connection - layers of communication
- Message Queuing Telemetry Transport (MQTT) - protocol, support IoT devices that connect in several different type of remote configuratons

### Message Queuing Telemetry Transport 
* Limited and constrained devices
- Simple implementation
- Lightweight, build for proproetary embedded systems
* Built for unreliable networks

## Challenges of IoT security




