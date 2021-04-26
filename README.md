# Enigma Simulator

An implementation of the Enigma machine in Python. Simulates a common 3-rotor machine
with the common 8 rotors and 3 reflectors.
[Wikipedia](https://en.wikipedia.org/wiki/Enigma_machine) has a good overview. Project
inspired by [this video](https://www.youtube.com/watch?v=RzWB5jL5RX0).

The transformation of each letter is implemented as a product of permutations
[(Rejewski, 1980)](https://www.worldcat.org/title/annales-polonici-mathematici/oclc/889386602),
in this case 26x26 matrices. The transform, in this formulation, can
therefore be expressed as (from Wikipedia):

![Enigma Transform](https://wikimedia.org/api/rest_v1/media/math/render/svg/e4244f8b3fb7118985e4f0b4b6accd4b7f5677b7)

Can be used to encrypt/decrypt messages ('X' was used to replace spaces):
```python
from enigma import Enigma


# Encrypting
enigma1 = Enigma(["I", "II", "III"], [0, 0, 0], [0, 0, 0], "B", "AD")
enigma1.encrypt("HELLOXWORLD") # Returns "ILBADSQQAPK"

# Decrypting
enigma2 = Enigma(["I", "II", "III"], [0, 0, 0], [0, 0, 0], "B", "AD")
enigma2.encrypt("ILBADSQQAPK") # Returns "HELLOXWORLD" back
```
