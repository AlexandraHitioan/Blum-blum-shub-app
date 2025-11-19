import os
import sys
from Crypto.Util import number

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

def main():
    p, q, n = generate_needed_blum_primes()

main()


