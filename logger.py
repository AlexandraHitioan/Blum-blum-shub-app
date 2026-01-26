import logging

LOG_FILE = "logs.txt"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

def log_key_generation(key: bytes):
    logging.info(
        f"KEY_GENERATED | key_hex={key.hex()} | key_bytes={key}"
    )

def log_encryption(input_file: str, output_dir: str, key: bytes):
    logging.info(
        f"ENCRYPT | key_hex={key.hex()} | input_file='{input_file}' | output_dir='{output_dir}'"
    )

def log_decryption(input_file: str, output_dir: str, key: bytes):
    logging.info(
        f"DECRYPT | key_hex={key.hex()} | input_file='{input_file}' | output_dir='{output_dir}'"
    )
