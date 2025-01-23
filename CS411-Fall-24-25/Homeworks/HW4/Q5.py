# NECESSARY DSA FUNCTIONS / LIBRARIES
# use "pip install sympy" if pyprimes is not installed
# use "pip install pycryptodome" if pycryptodome is not installed
import random
import sympy
import warnings
from Crypto.Hash import SHA3_256
from Crypto.Hash import SHAKE128

def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y
def modinv(a, m):
    if a < 0:
        a = a+m
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m

"""
MY SOLUTION BELOW
"""

# Set parameters
q = 897434149680309024926610536586679400252190817513
p = 97223004199266313523049166053330029092380541300786138924873181088471438705453794046370914345592432368059271294544102722787957310837797304650943069820520287549826630230617625792526214799206486444554607275157031742808122667064876655138748567945051878459968434840972135354745893868660267009794876094057307360271
g = 4621497210057935612371988511711932510361318115609980978853236984314561739819039313271820105098638480214293876477070872723831493769268422441714876014396954567136665583461293138792502100498181714605761615088670098808016625617309860858682957197265294737395362167975930097648958972424479880194787709852371142579
public_key = 45720223092558820344769930028614803638859051907129501277880999062740852114889610377894039520973053847174144955552627174266061939323577184681728281156812736603122999262209953001238229439108117677423857541271841004309469066208083385254271589636542160767902921803860270699359911081346969522186114311390226677995

message_1 = b"He who laugh last didn't get the joke"
r1 = 867552604169477346883674422144796797059303863627
s1 = 243861349833858115605937030382497401412336608822

message_2 = b"Ask me no questions, and I'll tell you no lies"
r2 = 686145019080375810998084468514665120375929537329
s2 = 774583422188330317252601038183072854135396118762


# Calculate inverse of s1 modulo q
s1_inv = modinv(s1, q)

# Calculate inverse of s2 * 2 modulo 1
s2_multiplied_by_2_inv = modinv(s2 * 2 % q, q)

# Calculate hash values
shake1 = SHAKE128.new(message_1)
H_m1 = int.from_bytes(shake1.read(q.bit_length() // 8), byteorder='big')

shake2 = SHAKE128.new(message_2)
H_m2 = int.from_bytes(shake2.read(q.bit_length() // 8), byteorder='big')

# Calculate a
a = (modinv(((r1 * s1_inv) % q) - ((r2 * s2_multiplied_by_2_inv) % q), q) * ((((H_m2 * s2_multiplied_by_2_inv) % q) - ((H_m1 * s1_inv) % q))) % q) % q

# Print a value
print(f"\nAlpha value is: {a}")


