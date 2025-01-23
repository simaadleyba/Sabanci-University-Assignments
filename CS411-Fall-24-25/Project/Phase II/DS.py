"""
CS411/507 - Cryptography | Fall 24/25
Term Project
Sima Adleyba - 28889
Seçil Gezer - 29145
"""


import random
from sympy import isprime
from Crypto.Hash import SHA3_256
import string
import os



# Generate q takes bit size of q as parameter (224 as default)
# It returns q, which is an 224 bit prime
def generate_q(q_bit = 224):

    # Set a flag
    generated_valid_q = False

    # While we have not generated
    while not generated_valid_q:

        # Generate a random q with q_bits size
        q_candidate = random.randrange(pow(2, (q_bit - 1)), pow(2, (q_bit)))

        # If random q is even, we add or subtract 1 to make it odd
        if q_candidate % 2 == 0:

            # Randomize the addition or subtraction
            temp = random.randint(0,1)

            if temp == 0:
                q_candidate += 1
            elif temp == 1:
                q_candidate -= 1


        # Check if the random q is prime and bit size is correct
        if isprime(q_candidate) and q_candidate.bit_length() == q_bit:

            # Set the flag true
            generated_valid_q = True

    # Return valid q candidate
    return q_candidate



# Generate g takes two prime (q and p) as parameters
# And returns g, which is a prime root in group G_q
def generate_g(q, p):

    # Set a flag
    generated_valid_g = False

    # While we have not generated a valid q
    while not generated_valid_g:

        # Generate a random alpha
        alpha = random.randint(2, p-2)

        # Set g using alpha
        g = pow(alpha, ((p-1) // q), p)

        # Check if g =/= 1 mod p
        if g % p != 1:

            # We generated a valid g, set the flag true
            generated_valid_g = True

    # Return the generator
    return g



# Setup for public parameter generation takes two arguments:
# q_bit and p_bit, which are 224 and 2048 respectively by default
# It returns q, p and g
def Setup(q_bit = 224, p_bit = 2048):

    # Generate a random p_bit (2048 bit) prime
    q = generate_q(q_bit)

    # Set a flag
    generated_valid_p = False

    # While we have not generated a valid prime p
    while not generated_valid_p:

        # Calculate the bit length for k
        k_bit = p_bit - q_bit

        # Generate k
        k = random.randrange(pow(2, k_bit - 1), pow(2, k_bit))

        # Generate p
        p = q * k + 1

        # Check if p is prime
        if isprime(p) and p.bit_length() == 2048:

            # We found a suitable p, set the flag True
            generated_valid_p = True

            # Generate g
            g = generate_g(q, p)

    # Return parameters
    return q, p, g



# Takes two primes (q, p) and g (primitive root in G_p) as parameters
# Computes and returns public key
def KeyGen(q, p, g):

    # Select a random a
    a = random.randint(1, q - 1)

    # Calculate beta
    beta = pow(g, a, p)

    return a, beta


# Takes message m, primes q and p, generator g and random secret key a as parameters
# Returns signature for m, which is tuple of s and h
def SignGen(m, q, p, g, a):

    # Generate a random k
    k = random.randint(1, q - 2)

    # Calculate r
    r = pow(g, k, p)

    # Convert r to bytes
    r_bytes = r.to_bytes((r.bit_length() + 7) // 8, byteorder='big')

    # Initialize h
    h = SHA3_256.new()

    # Concatenate message with r, update h
    h.update(m + r_bytes)

    # Convert h to int
    h = int.from_bytes(h.digest(), byteorder='big') % q

    # Calculate s
    s = (k - (a * h)) % q

    return s, h

# Takes message m, verification tuple s and h, primes q and p, generator g, and public key b as parameters
# Returns True if verified, False if not
def SignVer(m, s, h, q, p, g, b):


    # Calculate v
    g_to_s = pow(g, s, p)
    b_to_h = pow(b, h, p)
    v = (g_to_s * b_to_h) % p

    # Convert v to bytes
    v_bytes = v.to_bytes((v.bit_length() + 7) // 8, byteorder='big')

    # Calculate u
    u = SHA3_256.new()

    # Concatenate m with v, update u
    u.update(m + v_bytes)

    # Convert u to int
    u = int.from_bytes(u.digest(), byteorder='big') % q

    # Check if u is equal to h, and return the corresponding flag
    if u == h:
        return 0

    else:
        return -1


# Generate or read takes a filename (which is pubparams.txt) by default
# It reads the file if it exists, and returns q, p and g
# If file does not exist, it generates q, p and g, writes them to the file, and returns the parameters
def GenerateOrRead(filename="pubparams.txt"):

    # Check if the file exists
    if os.path.exists(filename):

        # Open the file
        try:
            with open(filename, 'r') as file:

                # Read parameters line by line
                q = int(file.readline().strip())
                p = int(file.readline().strip())
                g = int(file.readline().strip())

            # Return parameters
            return q, p, g

        except Exception as e:
            print(e)

    # If file does not exist
    else:

        # Generate parameters
        q, p, g = Setup()

        # Write to the file
        try:
            with open(filename, 'w') as file:
                file.write(f"{q}\n")
                file.write(f"{p}\n")
                file.write(f"{g}\n")

        except Exception as e:
            print(e)

        # Return parameters
        return q, p, g



# Takes length of a string, randomly select ascii characters and constructs a message
# Returns the message
def random_string(length):

    # Create an empty message
    message = ''

    # For the specified length
    for _ in range(length):

        # Select a random character
        rand_letter = random.choice(string.ascii_letters + string.digits + string.punctuation)

        # Append the message
        message += rand_letter

    # Return the message
    return message





