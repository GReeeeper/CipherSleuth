import tkinter as tk
from tkinter import ttk, messagebox
import base64
import string
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.fernet import Fernet

class DecrypterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CipherSleuth")
        self.root.geometry("800x700")
        
        # Theme configuration
        self.configure_styles()
        
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.algorithms = [
            "Auto-Detect",
            "Base64", 
            "Caesar Cipher", 
            "Vigenere Cipher", 
            "Fernet", 
            "AES-256-GCM"
        ]
        
        # Keep track of dynamic parameter widgets
        self.param_widgets = {}
        
        self.build_ui()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        bg_color = "#2d2d2d"
        fg_color = "#e0e0e0"
        accent_color = "#007acc"
        button_bg = "#3c3c3c"
        
        self.root.configure(bg=bg_color)
        
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=fg_color, font=("Consolas", 12))
        style.configure("TButton", background=button_bg, foreground=fg_color, font=("Consolas", 10), borderwidth=1)
        style.map("TButton", background=[('active', accent_color)])
        style.configure("TCombobox", fieldbackground="#333333", background="#3c3c3c", foreground="white")

    def build_ui(self):
        ttk.Label(self.main_frame, text="CIPHERSLEUTH", font=("Consolas", 18, "bold")).pack(pady=(0, 20))
        
        # Ciphertext Input
        ttk.Label(self.main_frame, text="Encrypted Message (Ciphertext):").pack(anchor=tk.W)
        self.cipher_text = tk.Text(self.main_frame, height=8, bg="#333333", fg="white", font=("Consolas", 11), insertbackground="white")
        self.cipher_text.pack(fill=tk.X, pady=(0, 15))
        self.cipher_text.bind("<KeyRelease>", self.on_type_auto_decrypt)
        
        # Algorithm Selection
        algo_frame = ttk.Frame(self.main_frame)
        algo_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(algo_frame, text="Encryption Type:").pack(side=tk.LEFT, padx=(0, 10))
        self.algo_var = tk.StringVar(value=self.algorithms[0])
        self.algo_cb = ttk.Combobox(algo_frame, textvariable=self.algo_var, values=self.algorithms, state="readonly", width=20, font=("Consolas", 11))
        self.algo_cb.pack(side=tk.LEFT)
        self.algo_cb.bind("<<ComboboxSelected>>", lambda e: self.build_params())
        
        # Parameters Frame
        self.params_frame = ttk.LabelFrame(self.main_frame, text="Decryption Parameters")
        self.params_frame.pack(fill=tk.X, pady=(0, 15), ipadx=10, ipady=10)
        
        self.build_params()
        
        # Action Buttons
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Button(btn_frame, text="DECRYPT MESSAGE", command=self.perform_decryption, style="Accent.TButton").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Clear Fields", command=self.clear_fields).pack(side=tk.LEFT)
        
        # Plaintext Output
        ttk.Label(self.main_frame, text="Decrypted Message (Plaintext):").pack(anchor=tk.W)
        self.plain_text = tk.Text(self.main_frame, height=8, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 11), insertbackground="white")
        self.plain_text.pack(fill=tk.X, pady=(0, 10))

    def build_params(self):
        for widget in self.params_frame.winfo_children():
            widget.destroy()
        self.param_widgets.clear()
        
        algo = self.algo_var.get()
        
        if algo == "Auto-Detect":
            ttk.Label(self.params_frame, text="No key required. Magic auto-detect will guess Hex, Base64, or Caesar.", font=("Consolas", 10, "italic")).pack(pady=5)
            
        elif algo == "Base64":
            ttk.Label(self.params_frame, text="No key required for Base64 decoding.", font=("Consolas", 10, "italic")).pack(pady=5)
            
        elif algo == "Caesar Cipher":
            self.add_param_entry("Shift Value (Integer):", "shift", width=15)
            ttk.Label(self.params_frame, text="Note: Shift specifies how many letters backwards to shift.", font=("Consolas", 9)).pack(anchor=tk.W)
            
        elif algo == "Vigenere Cipher":
            self.add_param_entry("Keyword:", "keyword", width=30)
            
        elif algo == "Fernet":
            self.add_param_entry("Key (Base64url 32-byte):", "key", width=50)
            
        elif algo == "AES-256-GCM":
            self.add_param_entry("Key (Hex 32-byte / 64-char):", "key", width=65)
            self.add_param_entry("Nonce (Hex 12-byte / 24-char):", "nonce", width=65)

    def add_param_entry(self, label_text, param_name, width=30):
        frame = ttk.Frame(self.params_frame)
        frame.pack(fill=tk.X, pady=5)
        ttk.Label(frame, text=label_text, width=32).pack(side=tk.LEFT, padx=(0, 10))
        entry = ttk.Entry(frame, width=width, font=("Consolas", 11))
        entry.pack(side=tk.LEFT)
        self.param_widgets[param_name] = entry

    def clear_fields(self):
        self.cipher_text.delete("1.0", tk.END)
        self.plain_text.delete("1.0", tk.END)
        for entry in self.param_widgets.values():
            entry.delete(0, tk.END)

    def on_type_auto_decrypt(self, event):
        if self.algo_var.get() == "Auto-Detect":
            # Avoid expensive operations if text is too short or just triggered by shift keys
            if event.keysym in ("Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R", "Caps_Lock"):
                return
            self.perform_decryption(silent=True)

    def perform_decryption(self, silent=False):
        ciphertext = self.cipher_text.get("1.0", tk.END).strip()
        if not ciphertext:
            if not silent:
                messagebox.showwarning("Input Error", "Please enter the ciphertext you wish to decrypt.")
            return
            
        algo = self.algo_var.get()
        self.plain_text.delete("1.0", tk.END)
        result = ""
        
        try:
            if algo == "Auto-Detect":
                self.auto_decrypt(ciphertext)
                return
                
            elif algo == "Base64":
                # Add padding if missing
                padded = ciphertext
                if len(padded) % 4 != 0:
                    padded += '=' * (4 - len(padded) % 4)
                result = base64.b64decode(padded).decode('utf-8', errors='replace')
                
            elif algo == "Caesar Cipher":
                shift_str = self.param_widgets["shift"].get()
                if not shift_str.lstrip('-').isdigit():
                    raise ValueError("Shift must be an integer.")
                shift = int(shift_str) % 26
                result = self.decrypt_caesar(ciphertext, shift)
                
            elif algo == "Vigenere Cipher":
                keyword = self.param_widgets["keyword"].get().strip()
                if not keyword.isalpha():
                    raise ValueError("Keyword must contain only letters.")
                result = self.decrypt_vigenere(ciphertext, keyword)
                
            elif algo == "Fernet":
                key = self.param_widgets["key"].get().strip().encode('utf-8')
                f = Fernet(key)
                result = f.decrypt(ciphertext.encode('utf-8')).decode('utf-8')
                
            elif algo == "AES-256-GCM":
                key_hex = self.param_widgets["key"].get().strip()
                nonce_hex = self.param_widgets["nonce"].get().strip()
                
                key = bytes.fromhex(key_hex)
                nonce = bytes.fromhex(nonce_hex)
                
                if len(key) != 32:
                    raise ValueError(f"AES-256 key must be exactly 32 bytes (got {len(key)} bytes).")
                
                aesgcm = AESGCM(key)
                
                # Assume ciphertext is hex, if fails try base64
                try:
                    cipher_bytes = bytes.fromhex(ciphertext)
                except ValueError:
                    cipher_bytes = base64.b64decode(ciphertext)
                
                result = aesgcm.decrypt(nonce, cipher_bytes, None).decode('utf-8')
            
            else:
                result = "Algorithm not implemented."
                
            self.plain_text.insert(tk.END, result)
            
        except Exception as e:
            if not silent:
                messagebox.showerror("Decryption Failed", f"Failed to decrypt the message using {algo}:\n\n{str(e)}")
            else:
                self.plain_text.insert(tk.END, f"[Error processing {algo} cipher in background]")

    def auto_decrypt(self, ciphertext):
        # 1. Check Hex
        try:
            if all(c in string.hexdigits for c in ciphertext) and len(ciphertext) % 2 == 0:
                result = bytes.fromhex(ciphertext).decode('utf-8')
                if any(c.isalpha() for c in result):
                    self.plain_text.insert(tk.END, f"[DETECTED: Hex Encoding]\n\n{result}")
                    return
        except Exception:
            pass

        # 2. Check Base64
        try:
            padded = ciphertext
            if len(padded) % 4 != 0:
                padded += '=' * (4 - len(padded) % 4)
            result = base64.b64decode(padded).decode('utf-8')
            if any(c.isalpha() for c in result):
                self.plain_text.insert(tk.END, f"[DETECTED: Base64 Encoding]\n\n{result}")
                return
        except Exception:
            pass
            
        # 3. Caesar Cipher Brute Force
        best_shift = 0
        best_score = -1
        best_text = ""
        common_words = {"the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it", "for", "not", "on", "with", "he", "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her", "she", "or", "an", "will", "my", "one", "all", "would", "there", "their", "what"}
        
        for shift in range(1, 26):
            decrypted = self.decrypt_caesar(ciphertext, shift)
            words = "".join([c if c.isalpha() else ' ' for c in decrypted]).lower().split()
            score = sum(10 for w in words if w in common_words)
            score += sum(1 for char in decrypted.lower() if char in "etaoinshrdlc")
            
            if score > best_score:
                best_score = score
                best_shift = shift
                best_text = decrypted
                
        if best_score > max(5, len(ciphertext) * 0.2): 
            self.plain_text.insert(tk.END, f"[DETECTED: Caesar Cipher (Shift {best_shift})]\n\n{best_text}")
            return
            
        # Failed to crack automatically
        msg = ("[FAIL: Could not automatically detect or crack ciphertext]\n\n"
               "If this is AES-256-GCM, Fernet, or Vigenere, you MUST provide the specific key in the corresponding algorithm tab. "
               "Modern cryptography is mathematically designed to be unbreakable without the correct key!")
        self.plain_text.insert(tk.END, msg)

    def decrypt_caesar(self, text, shift):
        result = []
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                # Decrypt is shift backwards
                decrypted = chr((ord(char) - base - shift) % 26 + base)
                result.append(decrypted)
            else:
                result.append(char)
        return "".join(result)
        
    def decrypt_vigenere(self, text, keyword):
        keyword = keyword.upper()
        result = []
        key_idx = 0
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                shift = ord(keyword[key_idx % len(keyword)]) - ord('A')
                decrypted = chr((ord(char) - base - shift) % 26 + base)
                result.append(decrypted)
                key_idx += 1
            else:
                result.append(char)
        return "".join(result)

if __name__ == "__main__":
    root = tk.Tk()
    
    # Optional: configure specific accent style
    style = ttk.Style(root)
    style.configure("Accent.TButton", background="#007acc", foreground="white", font=("Consolas", 10, "bold"))
    
    app = DecrypterApp(root)
    root.mainloop()
