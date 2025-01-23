"""
CS411/507 - Cryptography | Fall 24/25
Term Project
Sima Adleyba - 28889
Seçil Gezer - 29145
"""

import os
import random
from Crypto.Hash import SHA3_256

# PoW implementation from Phase 2 with minor changes:
# -> It takes nonce value to calculate PrevBlock's PoW
# -> It calculates nonce by itself if we are computing for current block
# -> It does not take a file name but content itself

def PoW(PoWLen, TxCnt, BlockContent, PrevPoW, nonce = None):



    # ----- Compute Merklee root

    # Set a list for hashes
    hashes = []

    # Loop over transactions
    for i in range(TxCnt):
        # Read the block
        block_lines = BlockContent[i * 9: (i + 1) * 9]
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

    # If we are computing for prev block, there will be a valid nonce value which we will use to computer this block's PoW
    if nonce is not None:

        # Convert nonce to bytes
        nonce_bytes = nonce.to_bytes((nonce.bit_length() + 7) // 8, byteorder='big')

        # Compute PoW value
        digest = H_r + PrevPoW.encode('utf-8') + nonce_bytes
        hash_obj = SHA3_256.new()
        hash_obj.update(digest)
        PoW_val = hash_obj.hexdigest()

    # If we are computing for current block, we will find the nonce ourselves, then compute the nonce
    else:

        # Loop until we find a valid nonce
        valid_nonce_found = False
        while not valid_nonce_found:

            # Get a random nonce
            nonce = random.randint(10 ** 38, 10 ** 39 - 1)

            # Convert nonce to bytes
            nonce_bytes = nonce.to_bytes((nonce.bit_length() + 7) // 8, byteorder='big')

            # Compute PoW value
            digest = H_r + PrevPoW.encode('utf-8') + nonce_bytes
            hash_obj = SHA3_256.new()
            hash_obj.update(digest)
            PoW_val = hash_obj.hexdigest()

            # Check if nonce starts with PoWLen zeros
            if PoW_val.startswith('0' * PoWLen):

                # If so, update the flag
                valid_nonce_found = True

    # Return nonce and PoW_val
    return nonce, PoW_val


# Takes PoWLen, TxCnt, block candidate and previous block as parameters
# Returns new block and previous PoW
def AddBlock2Chain(PoWLen, TxCnt, block_candidate, PrevBlock):

    # If this is the first block of the chain, set PoW to "00000000000000000000"
    if PrevBlock == '':
        PrevPoW = "00000000000000000000"

    # Use PrevBlock to compute its PoW
    else:

        # Get PrevBlock's PrevPoW
        prev_pow_line = PrevBlock[0].strip()
        PrevBlockPrevPoW = prev_pow_line.split(": ")[1]

        # Get Prev Nonce
        nonce_line = PrevBlock[1].strip()
        PrevNonce = int(nonce_line.split(": ")[1])

        # Set transaction lines
        tx_lines = PrevBlock[2:]

        # Compute PrevPoW
        _, PrevPoW = PoW(PoWLen, TxCnt, tx_lines, PrevBlockPrevPoW, PrevNonce)


    # Compute this block's nonce and PoW
    nonce, PoW_val = PoW(PoWLen, TxCnt, block_candidate, PrevPoW)

    # Build the new block's content
    block_content = "".join(block_candidate)
    prev_pow_line = f"Previous PoW: {PrevPoW}\n"
    nonce_line = f"Nonce: {nonce}\n"
    new_block_content = prev_pow_line + nonce_line + block_content

    # Return the new block content and PrevPoW
    return new_block_content, PrevPoW