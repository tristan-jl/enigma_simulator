# Enigma Simulator

An implementation of the Enigma machine in Python. Simulates a common 3-rotor machine
with the common 8 rotors and 3 reflectors.
[Wikipedia](https://en.wikipedia.org/wiki/Enigma_machine) has a good overview. Project
inspired by [this video](https://www.youtube.com/watch?v=RzWB5jL5RX0).

The transformation of each letter is implemented as a product of permutations
[(Rejewski, 1980)](https://www.impan.pl/pl/wydawnictwa/czasopisma-i-serie-wydawnicze/applicationes-mathematicae/all/16/4/102945/an-application-of-the-theory-of-permutations-in-breaking-the-enigma-cipher),
in this case 26x26 matrices. The transform, *E*, in this formulation, can
therefore be expressed as:

![Enigma Transform](docs/equation.svg)

where *P* is the plugboard, *L*, *M* and *R* are the left, middle and right rotors
respectively, *U* is the reflector and *p* is the cyclic permutation of the mapping of A
to B, B to C, etc. *a*, *b* and *c* are the rotations of each rotor as caused when a key
was pressed.

Can be used to encrypt/decrypt messages ('X' was used to replace spaces) as such:
```python
from enigma_simulator.enigma import Enigma


# Encrypting
enigma1 = Enigma(["I", "II", "III"], [1, 1, 1], "B", "AD", [0, 0, 0])
enigma1.encrypt("HELLOXWORLD") # Returns "LOFUHZZLZOB"

# Decrypting
enigma2 = Enigma(["I", "II", "III"], [1, 1, 1], "B", "AD", [0, 0, 0])
enigma2.encrypt("LOFUHZZLZOB") # Returns "HELLOXWORLD" back
```
