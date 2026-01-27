import tkinter as tk
from tkinter import filedialog, messagebox
from generateBlumPrimes import generate_aes_key
from encryption import AESEncryption
from logger import (
    log_key_generation,
    log_encryption,
    log_decryption,
)
from tkinter import ttk
from vulnerabilityGUI import vulnerabilityTab

class AESApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("AES Encryption with a Blum-Blum-Shub Key Generator")
        self.geometry("500x300")
        self.resizable(False, False)

        self.key_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):

        tabs = ttk.Notebook(self)

        encryption_tool_tab = tk.Frame(tabs)
        vulnerability_tab = tk.Frame(tabs)

        tabs.add(encryption_tool_tab, text="Encryption Tool")
        tabs.add(vulnerability_tab, text="Vulnerabilities")

        tabs.pack(expand = 1, fill ="both")

        key_frame = tk.Frame(encryption_tool_tab)
        key_frame.pack()

        tk.Label(key_frame, text="AES Key (hex)", font=("Arial", 11, "bold")).pack(pady=5)
        tk.Entry(key_frame, textvariable=self.key_var, width=50).pack(side=tk.LEFT, padx=5)
        tk.Button(key_frame, text="Generate Key", command=self.generate_key).pack(side=tk.LEFT)


        encryption_frame = tk.Frame(encryption_tool_tab)
        encryption_frame.pack()

        tk.Label(encryption_frame, text="Encryption", font=("Arial", 11, "bold")).pack(pady=10)
        tk.Button(encryption_frame, text="Encrypt File", width=25, command=self.encrypt_file).pack(pady=5)

        tk.Label(encryption_frame, text="Decryption", font=("Arial", 11, "bold")).pack(pady=10)
        tk.Button(encryption_frame, text="Decrypt File", width=25, command=self.decrypt_file).pack(pady=5)

        vulnerability_frame = vulnerabilityTab(vulnerability_tab)
        vulnerability_frame.pack()
    

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
