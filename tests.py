import unittest
import math
from Crypto.Random import get_random_bytes
from generateBlumPrimes import generate_bbs_seed, generate_bbs_bits

#first, we start with some small values
p1 = 7
q1 = 11
n1 = p1 * q1

expected_bits = 8
expected_bytes = b'\x66'

#we pick some larger constant from tests
BIG_N = 0x6c12b3eef0963829fb2f78531fca7ec581c7226e6d5d9f3d2744bcc842cd6dfed11c2af0d9c085f9d9bd05f88cbcccb2c15993bed83f81743838dd5b31198545

KNOWN_SEED_LARGE = 12345678901234567890123456789012345678901234567890
EXPECTED_KEY_128_HEX = "178f7cdbc83f2e05afa6ea6e06001814"

class TestBlum(unittest.TestCase):
    def test_small_seq(self):
        print("TEST 1")
        seed = 17
        key_bytes = generate_bbs_bits(n1, seed, expected_bits)
        self.assertEqual(len(key_bytes), 1, "Length of the key in bytes must be 1")
        self.assertEqual(key_bytes, expected_bytes, f"Expected value is {expected_bytes.hex()}, Obtained value: {key_bytes.hex()}")


    def test_bbs_large_key(self):
        print("TEST 2")
        seed = KNOWN_SEED_LARGE
        num_bits = 128
        key_bytes = generate_bbs_bits(BIG_N, seed, num_bits)
        self.assertEqual(len(key_bytes), num_bits//8, "Length of the key in bytes must be 16 bytes (128 bits)")
        self.assertEqual(key_bytes.hex(), EXPECTED_KEY_128_HEX,
                         f"Expected value: {EXPECTED_KEY_128_HEX}, Obtained value: {key_bytes.hex()}")


    def test_seed_generation_validity(self):
        print("TEST 3")
        for i in range(5):
            x0 = generate_bbs_seed(BIG_N)
            self.assertTrue(x0 > 1 and x0 < BIG_N - 1, "Seed must be 1 < x0 < N-1.")
            self.assertEqual(math.gcd(x0, BIG_N), 1, "Seed must be coprime with N (gcd=1).")


    def test_p_and_q_validity(self):
        print("TEST 4")
        p = 11
        q = 7
        self.assertTrue(p % 4 == 3, "p divided by 4 must have the remainder 3")
        self.assertTrue(q % 4 == 3, "q divided by 4 must have the remainder 3")



def main():
    unittest.main()