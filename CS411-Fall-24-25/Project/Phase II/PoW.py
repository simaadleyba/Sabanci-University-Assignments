"""
CS411/507 - Cryptography | Fall 24/25
Term Project
Sima Adleyba - 28889
Seçil Gezer - 29145
"""


import os
import random
from Crypto.Hash import SHA3_256



def CheckPow(p, q, g, PoWLen, TxCnt, filename):

    '''
    The function CheckPow returns an empty string if PoW of the block of transactions in “filename’ does not have preceding PoWLen hexadecimal 0s.
    Otherwise, it returns the value of PoW.
    '''

    # Check if the file exists
    if os.path.exists(filename):

        # Open the file and read lines
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()

        except Exception as e:
            print("File could not be opened:", e)

    # Set a list for hashes
    hashes = []

    # Get nonce
    nonce = int((lines[0].split(':'))[1].strip())

    # Update lines
    lines = lines[1:]

    # Loop over transactions
    for i in range(TxCnt):

        # Read the block
        block_lines = lines[i * 7 : (i + 1) * 7]
        block = "".join(block_lines).encode("utf-8")

        # Hash the block
        hash_obj = SHA3_256.new()
        hash_obj.update(block)
        hash = hash_obj.digest()

        # Add it to the hashes list
        hashes.append(hash)

    # ----- Merklee tree implementation

    # While we don't arrive at root
    while len(hashes) != 1:

        # Set a list to store hashes in the upper depth
        upper_hashes = []

        # Combine hashes two by two
        for i in range(len(hashes) // 2):

            # Combine hashes
            combined_hash = hashes[2 * i] + hashes[2 * i + 1]

            # Hash the combined value
            hash_obj = SHA3_256.new()
            hash_obj.update(combined_hash)
            hash = hash_obj.digest()

            # Add hash to the list
            upper_hashes.append(hash)

        # Update hashes list
        hashes = upper_hashes

    # Set Merklee root
    H_r = hashes[0]

    # Convert nonce to bytes
    nonce_bytes = nonce.to_bytes((nonce.bit_length() + 7) // 8, byteorder='big')

    # Compute SHA3_256 to get PoW
    PoW_val_obj = SHA3_256.new()
    PoW_val_obj.update(H_r + nonce_bytes)
    PoW_val = PoW_val_obj.hexdigest()

    # Return PoW

    # If it starts with PoWLen zeros, return PoW
    if PoW_val.startswith('0' * PoWLen):
        return PoW_val

    # If it does not, return an empty string
    else:
        return ''



def PoW(PoWLen, q, p, g, TxCnt, filename):

    '''
    Reads the transactions in filename (i.e., “transactions.txt” generated in Test 1) and computes a PoW (with len >= 5) for the block.
    After finds the PoW for the block, it appends the nonce at the beginning of the block and writes it into a file with the name “block.txt”.
    '''

    # Check if the file exists
    if os.path.exists(filename):

        # Open the file and read lines
        try:
            with open(filename, 'r') as file:
                file_content = file.read()
                lines = file.readlines()

        except Exception as e:
            print("File could not be opened:", e)

    # ----- Compute Merklee root

    # Set a list for hashes
    hashes = []

    # Loop over transactions
    for i in range(TxCnt):

        # Read the block
        block_lines = lines[i * 7 : (i + 1) * 7]
        block = "".join(block_lines).encode("utf-8")

        # Hash the block
        hash_obj = SHA3_256.new()
        hash_obj.update(block)
        hash = hash_obj.digest()

        # Add it to the list
        hashes.append(hash)

    # While we don't arrive at root
    while len(hashes) != 1:

        # Set a list to store hashes in the upper depth
        upper_hashes = []

        # Combine hashes two by two
        for i in range(len(hashes) // 2):

            # Combine hashes
            combined_hash = hashes[2 * i] + hashes[2 * i + 1]

            # Hash the combined value
            hash_obj = SHA3_256.new()
            hash_obj.update(combined_hash)
            hash = hash_obj.digest()

            # Add hashes to the list
            upper_hashes.append(hash)

        # Update hashes list
        hashes = upper_hashes

    # Set Merklee root
    H_r = hashes[0]

    # Loop until we find a valid nonce
    valid_nonce_found = False
    while not valid_nonce_found:

        # Get a random nonce
        nonce = random.randint(10 ** 38, 10 ** 39 - 1)

        # Convert nonce to bytes
        nonce_bytes = nonce.to_bytes((nonce.bit_length() + 7) // 8, byteorder='big')

        # Get SHA3_256 of nonce
        hash_obj = SHA3_256.new()
        hash_obj.update(H_r + nonce_bytes)
        PoW_val = hash_obj.hexdigest()

        # Check if nonce starts with PoWLen zeros
        if PoW_val.startswith('0' * PoWLen):

            # If so, update the flag
            valid_nonce_found = True

    # Append nonce to content and return it
    nonce_line = f"Nonce: {nonce}\n"
    content = nonce_line + "".join(lines)
    return content