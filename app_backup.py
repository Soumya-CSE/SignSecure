import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import hashlib

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature


# =========================
# Paths
# =========================

KEY_DIR = Path("keys")
SIGNATURE_DIR = Path("signatures")

KEY_DIR.mkdir(exist_ok=True)
SIGNATURE_DIR.mkdir(exist_ok=True)


# =========================
# Generate RSA Keys
# =========================

def generate_keys():

    try:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=3072
        )

        public_key = private_key.public_key()

        private_key_data = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_key_data = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        (KEY_DIR / "private_key.pem").write_bytes(private_key_data)
        (KEY_DIR / "public_key.pem").write_bytes(public_key_data)

        status_label.config(
            text="✅ RSA-3072 key pair generated!"
        )

        messagebox.showinfo(
            "Success",
            "RSA key pair generated successfully."
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


# =========================
# Select File
# =========================

def select_file():

    file_path = filedialog.askopenfilename()

    if file_path:

        selected_file.set(file_path)

        update_hash(file_path)

        status_label.config(
            text="📄 File selected successfully."
        )


# =========================
# SHA-256
# =========================

def calculate_sha256(file_path):

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:

        while chunk := file.read(4096):

            sha256.update(chunk)

    return sha256.hexdigest()


def update_hash(file_path):

    try:

        hash_value = calculate_sha256(file_path)

        hash_text.delete("1.0", tk.END)

        hash_text.insert(
            tk.END,
            hash_value
        )

    except Exception as e:

        messagebox.showerror(
            "Hash Error",
            str(e)
        )


# =========================
# Sign File
# =========================

def sign_selected_file():

    file_path = selected_file.get()

    if not file_path:

        messagebox.showwarning(
            "No File",
            "Please select a file first."
        )

        return

    private_key_path = KEY_DIR / "private_key.pem"

    if not private_key_path.exists():

        messagebox.showwarning(
            "Missing Key",
            "Generate RSA keys first."
        )

        return

    try:

        private_key = serialization.load_pem_private_key(
            private_key_path.read_bytes(),
            password=None
        )

        file_data = Path(file_path).read_bytes()

        signature = private_key.sign(
            file_data,

            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),

            hashes.SHA256()
        )

        signature_path = (
            SIGNATURE_DIR /
            f"{Path(file_path).name}.sig"
        )

        signature_path.write_bytes(signature)

        status_label.config(
            text="✍️ File signed successfully!"
        )

        messagebox.showinfo(
            "Success",
            f"Signature created:\n\n{signature_path}"
        )

    except Exception as e:

        messagebox.showerror(
            "Signing Error",
            str(e)
        )


# =========================
# Verify File
# =========================

def verify_selected_file():

    file_path = selected_file.get()

    if not file_path:

        messagebox.showwarning(
            "No File",
            "Please select a file first."
        )

        return

    public_key_path = KEY_DIR / "public_key.pem"

    signature_path = (
        SIGNATURE_DIR /
        f"{Path(file_path).name}.sig"
    )

    if not public_key_path.exists():

        messagebox.showwarning(
            "Missing Key",
            "Public key not found."
        )

        return

    if not signature_path.exists():

        messagebox.showwarning(
            "Missing Signature",
            "Signature file not found."
        )

        return

    try:

        public_key = serialization.load_pem_public_key(
            public_key_path.read_bytes()
        )

        file_data = Path(file_path).read_bytes()

        signature = signature_path.read_bytes()

        public_key.verify(

            signature,
            file_data,

            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),

            hashes.SHA256()
        )

        status_label.config(
            text="✅ SIGNATURE VALID — FILE INTEGRITY VERIFIED"
        )
        generate_security_report(
    file_path,
    True
) 

        messagebox.showinfo(
            "Verification Result",
            "✅ SIGNATURE VALID\n\n"
            "The file has not been modified."
        )

    except InvalidSignature:

        status_label.config(
            text="❌ SIGNATURE INVALID — FILE MAY BE MODIFIED"
        )
        generate_security_report(
    file_path,
    False
)
        

        messagebox.showerror(
            "Verification Result",
            "❌ SIGNATURE INVALID\n\n"
            "The file may have been modified."
        )

    except Exception as e:

        messagebox.showerror(
            "Verification Error",
            str(e)
        )

def generate_security_report(file_path, signature_status):

    file_path = Path(file_path)

    if not file_path.exists():
        return

    try:
        file_name = file_path.name
        file_size = file_path.stat().st_size
        sha256_hash = calculate_sha256(file_path)

        if signature_status:
            signature = "VALID"
            integrity = "VERIFIED"
            status = "SAFE"
        else:
            signature = "INVALID"
            integrity = "FAILED"
            status = "TAMPERED / UNTRUSTED"

        report = (
            "SIGNSECURE SECURITY REPORT\n"
            "====================================\n\n"
            f"File Name    : {file_name}\n"
            f"File Size    : {file_size} bytes\n\n"
            f"SHA-256      : {sha256_hash}\n\n"
            "Cryptography\n"
            "------------------------------------\n"
            "Algorithm    : RSA-3072 + SHA-256\n"
            "Padding      : RSA-PSS\n\n"
            "Verification\n"
            "------------------------------------\n"
            f"Signature    : {signature}\n"
            f"Integrity    : {integrity}\n"
            f"Status       : {status}\n"
        )

        report_text.delete("1.0", tk.END)
        report_text.insert(tk.END, report)

    except Exception as e:
        messagebox.showerror(
            "Report Error",
            str(e)
        )

# =========================
# GUI
# =========================

root = tk.Tk()

root.title(
    "SignSecure - Digital Signature System"
)

root.geometry("700x600")

root.resizable(False, False)


# Title

title_label = tk.Label(
    root,
    text="🔐 SignSecure",
    font=("Arial", 24, "bold")
)

title_label.pack(pady=10)


subtitle_label = tk.Label(
    root,
    text="Digital Signature & File Integrity Verification",
    font=("Arial", 12)
)

subtitle_label.pack()


# Selected file

selected_file = tk.StringVar()

file_frame = tk.Frame(root)

file_frame.pack(pady=20)


tk.Label(
    file_frame,
    text="Selected File:",
    font=("Arial", 11, "bold")
).pack(side=tk.LEFT)


file_entry = tk.Entry(
    file_frame,
    textvariable=selected_file,
    width=55
)

file_entry.pack(
    side=tk.LEFT,
    padx=10
)


select_button = tk.Button(
    root,
    text="📁 Select File",
    width=25,
    command=select_file
)

select_button.pack(pady=5)


# Key generation

key_button = tk.Button(
    root,
    text="🔑 Generate RSA Keys",
    width=25,
    command=generate_keys
)

key_button.pack(pady=5)


# Signing

sign_button = tk.Button(
    root,
    text="✍️ Sign File",
    width=25,
    command=sign_selected_file
)

sign_button.pack(pady=5)


# Verification

verify_button = tk.Button(
    root,
    text="🔍 Verify Signature",
    width=25,
    command=verify_selected_file
)

verify_button.pack(pady=5)


# Hash

tk.Label(
    root,
    text="SHA-256 Hash",
    font=("Arial", 11, "bold")
).pack(pady=(20, 5))


hash_text = tk.Text(
    root,
    height=3,
    width=75
)

hash_text.pack()


# Status

status_label = tk.Label(
    root,
    text="Status: Ready",
    font=("Arial", 11, "bold")
)

status_label.pack(pady=25)
# Security Report

tk.Label(
    root,
    text="Security Report",
    font=("Arial", 11, "bold")
).pack(pady=(15, 5))


report_text = tk.Text(
    root,
    height=10,
    width=75
)

report_text.pack()


# Start application

root.mainloop()
