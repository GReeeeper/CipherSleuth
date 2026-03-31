# CipherSleuth

CipherSleuth is a robust, local desktop application built in Python that intelligently decrypts and decodes various types of obfuscated text. Built with a sleek dark-mode graphical user interface via Tkinter, it allows you to automatically reverse-engineer simple ciphers or interactively decrypt mathematically secure encryption standards using keys.

## ✨ Features

- **Live Auto-Detect & Crack:** Intelligent parsing mode that attempts to instantly detect, decode, and brute-force the text automatically as you type.
- **Base64 Decoding:** Seamlessly reverses Base64 padding and encoding.
- **Hex Decoding:** Automatically detects and decodes hexadecimal strings into readable text.
- **Caesar Cipher:** Quickly brute-forces all 25 shift options and maps out the most probable text using frequency analysis and common English words.
- **Vigenere Cipher:** Manually decrypt using a provided keyword.
- **Fernet Encryption:** Securely reverse Fernet configurations using a standard url-safe Base64 32-byte key.
- **AES-256-GCM Encryption:** Advanced decryption of AES Galois/Counter Mode ciphertexts using a 32-byte Hex Key and a 12-byte Hex Nonce.

## 🚀 Installation & Usage

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone <your-repo-url>
   cd CipherSleuth
   ```

2. **Install dependencies**:
   ```bash
   pip install cryptography
   ```

3. **Run the utility**:
   ```bash
   python message_decrypter.py
   ```

## ⚠️ Notes on Cryptography

CipherSleuth can only automatically solve classical ciphers (such as Caesar, Hex, and Base64). Modern encryption protocols like **AES-256-GCM** and **Fernet** are mathematically intended to be impossible to reverse without the explicitly constructed key file/passphrase. You MUST provide the corresponding keys to view your text in those specific modes!
