# RSA OAEP FUNCTIONS
# use "pip install pyprimes" if pyprimes is not installed
# use "pip install pycryptodome" if pycryptodome is not installed
import math
import timeit
import random
import sympy
import warnings
from Crypto.Hash import SHA3_256
from Crypto.Hash import SHA3_384
from Crypto.Hash import SHA3_512
from Crypto.Hash import SHAKE128, SHAKE256


def egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    gcd = b
    return gcd, x, y


def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m


def random_prime(bitsize):
    warnings.simplefilter('ignore')
    chck = False
    while chck == False:
        p = random.randrange(2 ** (bitsize - 1), 2 ** (bitsize) - 1)
        chck = sympy.isprime(p)
    warnings.simplefilter('default')
    return p


k0 = 8
k1 = 128


def RSA_KeyGen(bitsize):
    p = random_prime(bitsize)
    q = random_prime(bitsize)
    N = p * q
    phi_N = (p - 1) * (q - 1)
    e = 2 ** 16 + 1
    while True:
        gcd, x, y = egcd(e, phi_N)
        if gcd == 1:
            break
        e = e + 2
    d = modinv(e, phi_N)
    return e, d, p, q, N


def RSA_OAEP_Enc(m, e, N, R):
    k = N.bit_length() - 2
    m0k1 = m << k1
    shake = SHAKE128.new(R.to_bytes(k0 // 8, byteorder='big'))
    GR = shake.read((k - k0) // 8)
    m0k1GR = m0k1 ^ int.from_bytes(GR, byteorder='big')
    shake = SHAKE128.new(m0k1GR.to_bytes((m0k1GR.bit_length() + 7) // 8, byteorder='big'))
    Hm0k1GR = shake.read(k0 // 8)
    RHm0k1GR = R ^ int.from_bytes(Hm0k1GR, byteorder='big')
    m_ = (m0k1GR << k0) + RHm0k1GR
    c = pow(m_, e, N)
    return c


def RSA_OAEP_Dec(c, d, N):
    k = N.bit_length() - 2
    m_ = pow(c, d, N)
    m0k1GR = m_ >> k0
    RHm0k1GR = m_ % 2 ** k0
    shake = SHAKE128.new(m0k1GR.to_bytes((m0k1GR.bit_length() + 7) // 8, byteorder='big'))
    Hm0k1GR = shake.read(k0 // 8)
    R = int.from_bytes(Hm0k1GR, byteorder='big') ^ RHm0k1GR
    shake = SHAKE128.new(R.to_bytes(k0 // 8, byteorder='big'))
    GR = shake.read((k - k0) // 8)
    m0k1 = m0k1GR ^ int.from_bytes(GR, byteorder='big')
    m = m0k1 >> k1
    return m

"""
MY SOLUTION BELOW
"""

# Get the ciphertext, public key and modulo
ciphertext = 13516634877046172939940899241734395131976001195335205383153480982703251868249
public_key  = 65537
modulo = 39046952359238172324044370069637197037683328477985992228432800875393523690127

# Set the flag
found_pin = False

# Brute force, while not found pin
while not found_pin:

    # Loop over all possible pin values
    for i in range (1000, 10000):

        # Calculate possible R values (8 bit unsigned integers)
        bit_length = 8
        start = 0
        end = 2 ** 8

        # Loop over possible R values
        for R in range(start, end):
            c_ = RSA_OAEP_Enc(i, public_key, modulo, R)

            # If it is equal to ciphertext, then we found the pin
            if c_ == ciphertext:

                # Print the pin and R value, mark flag, leave the loop
                print(f"\n**********\nFound the pin: {i}\nR value is: {R}\n**********\n")
                found_pin = True


