#
# Depenndencies
#

import os
import sys
import random
import hashlib
import requests
import multiprocessing
from uuid import uuid4
from timeit import default_timer as timer

#
# Define methods
#

def proof_of_work(last_proof, seed):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    - Note:  We are adding the hash of the last proof to a number/nonce for the new proof
    """

    start = timer()

    print(f"Searching for next proof! (seed: {seed})")
    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1 + seed

    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the proof?

    IE:  last_hash: ...AE9123456, new hash 123456888...
    """

    last_guess = f'{last_proof}'.encode()
    last_guess_hash = hashlib.sha256(last_guess).hexdigest()

    guess = f'{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    return last_guess_hash[len(last_guess_hash)-6:] == guess_hash[:6]

def work(seed):
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"
        # node = "https://lambda-coin-test-1.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    id_path = os.path.join(os.path.dirname(__file__), 'my_id.txt')
    f = open(id_path, "r")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        #=> {'proof': 23478042, 'difficulty': 6}
        print(f"Last proof: {data['proof']}")
        new_proof = proof_of_work(data.get('proof'), seed)

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))


#
# Start mining blocks for coins
#

if __name__ == '__main__':
    jobs = []
    for i in range(1,7):
        p = multiprocessing.Process(target=work, args=(i**i,))
        jobs.append(p)
        p.start()

    # for i in range(1,7):
    #     p = multiprocessing.Process(target=work, args=(-i**i,))
    #     jobs.append(p)
    #     p.start()
