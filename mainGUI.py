import tkinter as tk
from tkinter import filedialog, messagebox
from generateBlumPrimes import generate_aes_key
from encryption import AESEncryption
from logger import (
    log_key_generation,
    log_encryption,
    log_decryption,
)


class AESApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("AES Encryption with a Blum-Blum-Shub Key Generator")
        self.geometry("500x300")
        self.resizable(False, False)

        self.key_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="AES Key (hex)", font=("Arial", 11, "bold")).pack(pady=5)

        key_frame = tk.Frame(self)
        key_frame.pack()

        tk.Entry(key_frame, textvariable=self.key_var, width=50).pack(side=tk.LEFT, padx=5)
        tk.Button(key_frame, text="Generate Key", command=self.generate_key).pack(side=tk.LEFT)

        tk.Label(self, text="Encryption", font=("Arial", 11, "bold")).pack(pady=10)
        tk.Button(self, text="Encrypt File", width=25, command=self.encrypt_file).pack(pady=5)

        tk.Label(self, text="Decryption", font=("Arial", 11, "bold")).pack(pady=10)
        tk.Button(self, text="Decrypt File", width=25, command=self.decrypt_file).pack(pady=5)


    def generate_key(self):
        key = generate_aes_key()
        self.key_var.set(key.hex())
        log_key_generation(key)
        messagebox.showinfo("Key Generated", "AES key generated successfully.")

    def encrypt_file(self):
        try:
            key = bytes.fromhex(self.key_var.get())
            aes = AESEncryption(key)

            input_file = filedialog.askopenfilename(title="Select file to encrypt")
            if not input_file:
                return

            output_dir = filedialog.askdirectory(title="Select output directory")
            if not output_dir:
                return

            aes.encrypt(input_file, output_dir)
            log_encryption(input_file, output_dir, key)
            messagebox.showinfo("Success", "File encrypted successfully.")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decrypt_file(self):
        try:
            key = bytes.fromhex(self.key_var.get())
            aes = AESEncryption(key)

            input_file = filedialog.askopenfilename(
                title="Select file to decrypt",
                filetypes=[("Encrypted files", "*.enc")]
            )
            if not input_file:
                return

            output_dir = filedialog.askdirectory(title="Select output directory")
            if not output_dir:
                return

            aes.decrypt(input_file, output_dir)
            log_decryption(input_file, output_dir, key)
            messagebox.showinfo("Success", "File decrypted successfully.")

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = AESApp()
    app.mainloop()
