from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from pathlib import Path
import sys


PRIVATE_KEY = Path("keys/private_key.pem")
SIGNATURE_DIR = Path("signatures")

SIGNATURE_DIR.mkdir(exist_ok=True)


def sign_file(file_path):

    file_path = Path(file_path)

    if not file_path.exists():
        print("❌ File not found.")
        return

    # Load private key
    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY.read_bytes(),
        password=None
    )

    # Read file
    file_data = file_path.read_bytes()

    # Generate digital signature
    signature = private_key.sign(
        file_data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Create signature filename
    signature_path = SIGNATURE_DIR / f"{file_path.name}.sig"

    # Save signature
    signature_path.write_bytes(signature)

    print("===================================")
    print("          SIGNSECURE")
    print("===================================")
    print("✅ File signed successfully!")
    print()
    print("File      :", file_path)
    print("Signature :", signature_path)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage:")
        print("python sign_file.py <file>")
    else:
        sign_file(sys.argv[1])
        