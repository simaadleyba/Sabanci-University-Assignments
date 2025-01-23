"""
CS411/505 - Cryptography | Fall 24/25
Term Project Phase I
Sima Adleyba - 28889
Seçil Gezer - 29145
"""


import random
import DS  # to use digital signature functions



"""
The function takes parameters q, p and g and generates public-private key pairs for both the payer and the payee.
The sender's private key payer_alpha and public key payer_beta are generated, and only the payee's public key is used.
"""


"""
The signing procedure is applied with the digital signature algorithm.
The signature is created using the converted byte version of the message, q, p, g parameters and payer_alpha, and as a result, s and h representing the signature are obtained.
"""

def gen_random_tx(q, p, g):
    payer_alpha, payer_beta = DS.KeyGen(q, p, g)  # Generates payer's private and public key
    _, payee_beta = DS.KeyGen(q, p, g)  # Generates payee's public key

    serial_number = random.getrandbits(128)  # Generates a random 128 bit serial number
    amount = random.randint(1, 1000000)  # Generates a random transaction amount



    message_to_sign = (  # Constructs the message fields to be signed
        f"Serial number: {serial_number}\n"
        f"Amount: {amount}\n"
        f"Payee public key (beta): {payee_beta}\n"
        f"Payer public key (beta): {payer_beta}\n"
    )


    s, h = DS.SignGen(message_to_sign.encode('utf-8'), q, p, g, payer_alpha)  # Generates signature s and h using payer's private key


    transaction = (  # Constructs the transaction with all required fields
        "*** Bitcoin transaction ***\n"
        f"Signature (s): {s}\n"
        f"Signature (h): {h}\n"
        f"Serial number: {serial_number}\n"
        f"Amount: {amount}\n"
        f"Payee public key (beta): {payee_beta}\n"
        f"Payer public key (beta): {payer_beta}\n"
    )

    return transaction