import unittest
import math
from Crypto.Random import get_random_bytes
from generateBlumPrimes import generate_bbs_seed, generate_bbs_bits
from encryption import AESEncryption
from generateBlumPrimesVulnerable import break_bbs_reverse
import os
from pathlib import Path

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

# Test for encryption & decryption
HARDCODED_KEY_128 = b'\xe4\x1dJ_Y\x8f\xd3\xce\xeaX*m\x99*-\x14'

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

    def test_encryption_decryption(self):
        print("TEST 5")

        aes = AESEncryption(HARDCODED_KEY_128)

        # Creating test_data path if doesn't exist, already in .gitignore file
        folder_path = Path("test_data")
        plaintext_path = folder_path / "test.txt"
        ciphertext_path = folder_path / "test.txt.enc"
        decrypted_path = folder_path / "decrypted_test.txt"

        if not folder_path.exists():
            folder_path.mkdir()

        # Writing dummy text to file
        with open(plaintext_path, "w", encoding="utf-16") as f:
            for i in range(10):
                content = f"{i}: Testing the encryption of data Ăă Îî Ââ Șș Țț this needs to match the decrypted text\n"
                f.write(content)

        # Encrypting
        aes.encrypt(plaintext_path, folder_path)
        # Decrypting
        aes.decrypt(ciphertext_path, folder_path)

        # Comparing all three
        with open(plaintext_path, "r", encoding="utf-16") as f1, open(decrypted_path, "r", encoding="utf-16") as f2:
            plaintext_contents = f1.read()
            decrypted_contents = f2.read()
            
        self.assertEqual(plaintext_contents, decrypted_contents, "Plaintext does not match decrypted contents")

    def test_vulnerability(self):
        print("TEST 6")

        # MATCH THIS
        original_key_hex = "264ba9ee03d1d366dcb35a1c79b86033"

        p = 69348563696518645831799359538811049101486969707615325680252191995549035903623
        q = 100949257235388876418383985207124635310299706713166943344156890574075911610267
        final_state = 5946192998409869876137142399927182142054923455588891833570257502318142699157078476720497326065378068314489701139348353186433223315328510905637899058548437

        broken_key = break_bbs_reverse(p, q, final_state).hex()

        self.assertEqual(original_key_hex, broken_key, "Original and broken key do not match")


if __name__ == "__main__":
    unittest.main()