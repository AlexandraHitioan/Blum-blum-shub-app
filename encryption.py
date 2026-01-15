from Crypto.Cipher import AES
from pathlib import Path

class AESEncryption:
    """
    Implements AES Encryption using the Cryptodome library
    """

    CHUNK_SIZE = 32768 # 32kb at a time

    def __init__(self, key : bytes):
        """
        Constructor for AESEncryption implementation

        :param bytes key: A 16 bytes key
        """

        if len(key) != 16:
            raise ValueError("Key length must be 16 bytes")
        self.key = key

    def encrypt(
            self
            , file_path: str
            , ciphertext_folder_path: str
            , ciphertext_file_name: str=None
        ) -> None:
        """
        Encrypts a file using self.key

        :param str file_path: Path to the file to encrypt
        :param str ciphertext_folder_path: Path to the folder to store the ciphertext
        :param str ciphertext_file_name: Name of the ciphertext file
        """

        plaintext_path = Path(file_path)
        ciphertext_folder_path = Path(ciphertext_folder_path)

        # Check if the file exists
        if not plaintext_path.is_file():
            raise FileNotFoundError(f"File path does not exist")
        
        # Check if the target folder exists
        if not ciphertext_folder_path.exists():
            raise FileNotFoundError(f"Folder path does not exist")
        
        # Set default name to a original file name + .enc
        if ciphertext_file_name is None:
            ciphertext_file_name = plaintext_path.name + ".enc"

        # Create full path for the file encryption
        ciphertext_path: Path = ciphertext_folder_path / ciphertext_file_name

        # ENCRYPTING THE TEXT

        with open(plaintext_path, "rb") as f_plain, open(ciphertext_path, "wb") as f_cipher:

            aes = AES.new(key=self.key, mode=AES.MODE_GCM)
            nonce = aes.nonce

            f_cipher.write(nonce)

            # Until the end of the plaintext, encrypt in chunks
            while chunk := f_plain.read(self.CHUNK_SIZE):
                ciphertext = aes.encrypt(chunk)
                f_cipher.write(ciphertext)

            # Write tag at the end of the file
            tag = aes.digest()
            f_cipher.write(tag)


    def decrypt(
            self
            , file_path: str
            , decrypted_folder_path: str
            , decrypted_file_name: str=None
        )  -> None:
        """
        Decrypts a file using self.key

        :param str file_path: Path to the file to decrypt
        :param str decrypted_folder_path: Path to the folder to store the plaintext
        :param str decrypted_file_name: Name of the file for the plaintext
        """

        ciphertext_path = Path(file_path)
        decrypted_folder_path = Path(decrypted_folder_path)

        # Check if the file exists
        if not ciphertext_path.is_file():
            raise FileNotFoundError(f"File path does not exist")
        
        if ciphertext_path.suffix != ".enc":
            raise FileNotFoundError(f"File is not using the .enc extension")
        
        # Check if the target folder exists
        if not decrypted_folder_path.exists():
            raise FileNotFoundError(f"Folder path does not exist")
        
        # Set default name to a original file name without .enc
        if decrypted_file_name is None:
            decrypted_file_name = "decrypted_" + ciphertext_path.stem

        decrypted_path: Path = decrypted_folder_path / decrypted_file_name


        # DECRYPTING THE TEXT
        # Calculating the file size minus the tag
        ciphertext_end = ciphertext_path.stat().st_size - 16

        with open(ciphertext_path, "rb") as f_cipher, open(decrypted_path, "wb") as f_plain:
            # Nonce needed to decrypt
            nonce = f_cipher.read(16)
            aes = AES.new(key=self.key, mode=AES.MODE_GCM, nonce=nonce)

            # Until the end of the ciphertext, decrypt bit by bit in chunks
            while f_cipher.tell() < ciphertext_end:
                    
                # This logic avoids accidently reading the tag at the end
                to_read = min(16, ciphertext_end - f_cipher.tell())
                plaintext = aes.decrypt(f_cipher.read(to_read))
                f_plain.write(plaintext)


            # Read tag at the end of the file
            tag = f_cipher.read(16)

            try:
                aes.verify(tag)
            except ValueError:
                raise PermissionError("Key is wrong or the ciphertext has been tampered with.")