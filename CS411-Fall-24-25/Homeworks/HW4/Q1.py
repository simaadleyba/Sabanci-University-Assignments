import math
import warnings
import sympy
import random

# Random Prime implementation from RSA_OAEP.py
def random_prime(bitsize):
    warnings.simplefilter('ignore')
    chck = False
    while chck == False:
        p = random.randrange(2**(bitsize-1), 2**(bitsize)-1)
        chck = sympy.isprime(p)
    warnings.simplefilter('default')
    return p

# Modinv implementation from RSA_OAEP.py
def modinv(a, m):
    # Extended Euclidean Algorithm to calculate modular inverse
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m

# RSA_Oracle_client functions
import random
import requests
from random import randint

API_URL = 'http://harpoon1.sabanciuniv.edu:9999'
my_id = 28889

def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m
def RSA_Oracle_Get():
  response = requests.get('{}/{}/{}'.format(API_URL, "RSA_Oracle", my_id))
  c, N, e = 0,0,0
  if response.ok:
    res = response.json()
    print(res)
    return res['c'], res['N'], res['e']
  else:
    print(response.json())

def RSA_Oracle_Query(c_):
  response = requests.get('{}/{}/{}/{}'.format(API_URL, "RSA_Oracle_Query", 28889, c_))
  print(response.json())
  m_= ""
  if response.ok:	m_ = (response.json()['m_'])
  else: print(response)
  return m_

def RSA_Oracle_Checker(m):
  response = requests.put('{}/{}/{}/{}'.format(API_URL, "RSA_Oracle_Checker", 28889, m))
  print(response.json())

"""
MY SOLUTION BELOW
"""

# Get ciphertext, modulo, and public key
c, N, e = RSA_Oracle_Get()

# Choose a random value that is relatively prime to N
random_value = random_prime(8)

# Calculate a value to raise
val_to_raise = pow(random_value, e, N)

# Raise the ciphertext
raised_ciphertext = (c * val_to_raise) % N

# Get the corresponding message for raised ciphertext
raised_message = RSA_Oracle_Query(raised_ciphertext)

# Recover the original message
message = (raised_message * modinv(random_value, N)) % N

# Convert the plaintext number into bytes
message = message.to_bytes((message.bit_length() + 7) // 8, byteorder='big')
print(f"\n**********\nMessage is:\n'{message.decode('utf-8')}'\n**********\n")

# Check the result
RSA_Oracle_Checker(message.decode("utf-8"))
