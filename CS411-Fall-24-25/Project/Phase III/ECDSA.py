"""
CS411/507 - Cryptography | Fall 24/25
Term Project
Sima Adleyba - 28889
Seçil Gezer - 29145
"""


import random
import sys
from ecpy.curves import Curve
import random
from sympy import isprime
import string
from Crypto.Hash import SHA3_256
import os



# Takes curve object E as parameter
# Returns private key sA, and public key QA
def KeyGen(E):

    # Get the order of the curve and generator
    n = E.order
    P = E.generator

    # Select a random number in range [1, order - 1]
    sA = random.randint(2, n - 1)

    # Get public key QA by multiplying generator with private key
    QA = sA * P

    return sA, QA



# Takes message m, curve object E, and private key sA as parameters
# Returns the tuple (s, h)
def SignGen(m, E, sA):

    # Get the order and generator of the curve
    n = E.order
    P = E.generator

    # Generate a random k in [1, n-1]
    k = random.randint(1, n - 1)

    # Compute the elliptic curve point R = k * P
    R = k * P

    # Get x-coordinate of R
    R_x = R.x

    # Convert R_x to bytes
    R_x_bytes = R_x.to_bytes((R_x.bit_length() + 7) // 8, byteorder='big')

    # Initialize hash object
    h_obj = SHA3_256.new()

    # Concatenate m with R_x
    h_obj.update(m + R_x_bytes)

    # Get h value
    h = int.from_bytes(h_obj.digest(), byteorder='big') % n

    # Calculate s
    s = (k - sA * h) % n

    # Ensure that s is not 0 (re-run in such case)
    if s == 0:
        return SignGen(m, E, sA)

    return s, h


# Takes message m, verification tuple s and h, curve object E, and public key QA
# Returns 0 if the signature is verified, -1 if not verified
def SignVer(m, s, h, E, QA):

    # Get the order and generator of the curve
    n = E.order
    P = E.generator

    # Compute the elliptic curve point V
    V = (s * P) + (h * QA)

    # Get x-coordinate of V
    V_x = V.x

    # Convert V_x to bytes
    V_x_bytes = V_x.to_bytes((V_x.bit_length() + 7) // 8, byteorder='big')

    # Initialize a hash object
    u_obj = SHA3_256.new()

    # Concatenate message m with V_x
    u_obj.update(m + V_x_bytes)

    # Get u value
    u = int.from_bytes(u_obj.digest(), byteorder='big') % n

    # Check if u is equal to h, and return the corresponding flag
    if u == h:
        return 0

    else:
        return -1








