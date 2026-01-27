from generateBlumPrimes import generate_needed_blum_primes,  generate_bbs_seed
import math
from sympy.ntheory.modular import crt

# Different version of the function that leaks the final state
def generate_bbs_bits_vulnerable(n, seed, nr_bits):
    xi = seed
    bit_seed = []

    if xi <= 1 or xi >= n - 1 or math.gcd(xi, n) != 1:
        print("[ERROR]: Seed is not valid. It should be coprime with n and different from 0 and 1")

    for _ in range(nr_bits):
        xi = pow(xi, 2)
        xi %= n
        bit = xi % 2
        bit_seed.append(bit)

    bit_seq = ''.join(str(bit) for bit in bit_seed)
    key = int(bit_seq, 2)

    #there's a formula by which we calculate this: the number of bytes needed to store the number of bits procided as parameters has to be round
    byte_length = (nr_bits + 7) // 8

    #we transform the generated key into bytes
    key_bytes = key.to_bytes(byte_length, byteorder='big')

    return key_bytes, xi


# Returns the key along with p, q, and the final state
def generate_aes_key_vulnerable():
    """
        Generates an AES key using the Blum Blum Shub implementation of 128 bits 
        - But leaks N and the final state to demonstrate how to break Blum Blum Shub
    """
    p, q, n = generate_needed_blum_primes()

    seed = generate_bbs_seed(n)
    aes_key, final_state = generate_bbs_bits_vulnerable(n, seed, 128)

    return aes_key, p, q, final_state

def break_bbs_reverse(p, q, final_state):
    """
        Breaks Blum Blum Shub when knowing N
    """

    reversed_engineered_key = str(final_state % 2)
    prev_state = final_state

    for _ in range(127):

        # STEP 1:
        # Calculate the principle root using p & q
        # state ^ (p + 1 / 4) mod p
        # state ^ (q + 1 / 4) mod q
        r1 = pow((prev_state), (p + 1) // 4, p)
        r2 = pow((prev_state), (q + 1) // 4, q)

        # STEP 2:
        # Use chinese remainder theorum to solve X
        # X = r1 mod 7
        # X = r1 mod 3
        # There are other roots, but the principle root is used in BBS
        crt_res = crt([p, q], [r1, r2])

        prev_state = crt_res[0]

        reversed_engineered_key = str(prev_state % 2) + reversed_engineered_key

    return int(reversed_engineered_key, 2).to_bytes(16, byteorder='big')