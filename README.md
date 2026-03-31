# CipherSleuth

CipherSleuth is a robust, local desktop application built in Python that intelligently decrypts and decodes various types of obfuscated text. Built with a sleek dark-mode graphical user interface via Tkinter, it allows you to automatically reverse-engineer simple ciphers or interactively decrypt mathematically secure encryption standards using keys.

## ✨ Features

- **Live Auto-Detect & Crack:** Intelligent parsing mode that attempts to instantly detect, decode, and brute-force the text automatically as you type.
- **Base64 Decoding:** Seamlessly reverses Base64 padding and encoding.
- **Hex Decoding:** Automatically detects and decodes hexadecimal strings into readable text.
- **Caesar Cipher:** Quickly brute-forces all 25 shift options and maps out the most probable text using frequency analysis and common English words.
- **Vigenere Cipher:** Automatically brute-forces using dictionary attacks, or manually decrypt using a provided keyword.
- **Fernet Encryption:** Features a dictionary attack to attempt recovering weak keys, or securely reverse using a standard url-safe Base64 32-byte key.
- **AES-256-GCM Encryption:** Simulates a brute-force dictionary attack on weak keys, or securely decrypt AES Galois/Counter Mode via a 32-byte Hex Key and a 12-byte Hex Nonce.
- **DES, Blowfish, & ARC4:** Native decryption support integrated directly from the powerful PyCryptodome library.
- **Custom Dictionary Attacks:** Power up the Auto-Detect mode by downloading the massive Top 10,000 SecLists common passwords list straight into memory, or load your own custom `.txt` wordlist for cracking!

## 🚀 Installation & Usage

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <your-repo-url>
   cd CipherSleuth
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the utility**:
   ```bash
   python message_decrypter.py
   ```

## ⚠️ Notes on Cryptography

CipherSleuth can automatically solve classical ciphers (such as Caesar, Hex, and Base64). By downloading or loading custom wordlists, you can also seamlessly execute **Dictionary Attacks** against Vigenere, AES-256-GCM, Fernet, ARC4, and more! 

However, remember that modern encryption protocols are mathematically intended to be impossible to reverse. If the encrypted text does not use a weak or compromised password within your loaded dictionary, you MUST provide the explicitly constructed key file/passphrase to decrypt it.
