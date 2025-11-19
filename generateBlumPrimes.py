import os
import sys

from Crypto.Random import get_random_bytes
from Crypto.Util import number
import math

nr_bit_size = 256
min_bit_size = 512

def is_prime(n):
    return ( n % 4 ) == 3


def generate_blum_prime(nr_bits):
    while True:
        nr = number.getPrime(nr_bits, os.urandom)
        #checking if the number satisfies the blum condition:
        if is_prime(nr):
            return nr


def generate_needed_blum_primes():
    #generates two distinct p and q primes and calculates the modulus N
    p = generate_blum_prime(nr_bit_size)
    while True:
        q = generate_blum_prime(nr_bit_size)
        if q != p:
            break

    n = p * q
    #Documentation Output
    print ("DOCUMENTATION")
    print("DOCUMENTATION:")
    print (f"P: {p}")
    print(f"Q: {q}")
    print(f"N: {n}")
    print(f"Prime p (hex): {hex(p)}")
    print(f"Condition p mod 4: {p % 4}")
    print(f"Prime q (hex): {hex(q)}")
    print(f"Condition q mod 4: {q % 4}")
    print(f"Modulus N (p * q) (hex): {hex(n)}")

    print(f"\n[VERIFIED] Both primes satisfy p ≡ 3 (mod 4).")
    print(f"[VERIFIED] Modulus N has {n.bit_length()} bits.")
    return p, q, n




#-----------------------------GENERATING THE BBS BITS FUNCTION---------------------------------

def generate_bbs_bits(n, seed, nr_bits):
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
    return key_bytes




#-----------------------------GENERATE THE SEED FOR THEY BBS KEY -----------------------------------------------
def generate_bbs_seed(n):
    seed_bytes = get_random_bytes(32)
    x0 = int.from_bytes(seed_bytes, byteorder='big') % n

    #we will regenerate the seed if it does not respect the BBS rules
    while x0 == 1 or x0 == 0 or x0 >= n -1 or math.gcd(x0, n) != 1:
        seed_bytes = get_random_bytes(32)
        x0 = int.from_bytes(seed_bytes, byteorder='big') % n

    return x0



def main():
    p, q, n = generate_needed_blum_primes()
    seed = generate_bbs_seed(n)
    aes_key = generate_bbs_bits(n, seed, 128)

    print("\n--- Generate BBS key: Test ---")
    if aes_key:
        print(f"Nr of bytes generated: {len(aes_key)}")
        print(f"AES 128 key (Hex): {aes_key.hex()}")

main()


