import random
from lfsr import LFSR, FindPeriod, BM

print("\n------------------------")
""" x^6 + x^5 + x^4 + x + 1 """

length = 256

L = 6
C = [0] * (L + 1)
S = [0] * L

# Set polynomial
C[0] = 1  # Constant term
C[1] = 1  # x term
C[4] = 1  # x^4 term
C[5] = 1  # x^5 term
C[6] = 1  # x^6 term


# Set a random initial state
for i in range(0,L):
    S[i] = random.randint(0, 1)
print ("Initial state: ", S)

keystream = [0]*length
for i in range(0,length):
     keystream[i] = LFSR(C, S)


period = FindPeriod(keystream)
print ("First period: ", period)
print ("L and C(x): ", BM(keystream))
print ("keystream: ", keystream)

# Check if period is 2^L - 1 where L is the degree of polynomial
if period == (2 ** L - 1):
    print("x^6 + x^5 + x^4 + x + 1 generates maximum period sequences.")

else:
    print("x^6 + x^5 + x^4 + x + 1 does not generate maximum period sequences.")

print("\n------------------------")
""" x^5 + x^3 + x^2 + 1 """


length = 256

L = 5
C = [0] * (L + 1)
S = [0] * L

# Set polynomial
C[0] = 1  # Constant term
C[2] = 1  # x^2 term
C[3] = 1  # x^3 term
C[5] = 1  # x^5 term


# Set a random initial state
for i in range(0,L):
    S[i] = random.randint(0, 1)
print ("Initial state: ", S)

keystream = [0]*length
for i in range(0,length):
     keystream[i] = LFSR(C, S)


period = FindPeriod(keystream)
print ("First period: ", period)
print ("L and C(x): ", BM(keystream))
print ("keystream: ", keystream)

# Check if period is 2^L - 1 where L is the degree of polynomial
if period == (2 ** L - 1):
    print("x^5 + x^3 + x^2 + 1 generates maximum period sequences.")

else:
    print("x^5 + x^3 + x^2 + 1 does not generate maximum period sequences.")


print("\n------------------------")
""" x^5 + x^3 + 1 """

length = 256

L = 5
C = [0] * (L + 1)
S = [0]*L

# Set polynomial
C[0] = 1  # Constant term
C[3] = 1  # x^3 term
C[5] = 1  # x^5 term

# Set a random initial state
for i in range(0,L):
    S[i] = random.randint(0, 1)
print ("Initial state: ", S)

keystream = [0]*length
for i in range(0,length):
     keystream[i] = LFSR(C, S)


period = FindPeriod(keystream)
print ("First period: ", period)
print ("L and C(x): ", BM(keystream))
print ("keystream: ", keystream)

# Check if period is 2^L - 1 where L is the degree of polynomial
if period == (2 ** L - 1):
    print("x^5 + x^3 + 1 generates maximum period sequences.")

else:
    print("x^5 + x^3 + 1 does not generate maximum period sequences.")

