from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from pathlib import Path
import sys


PUBLIC_KEY = Path("keys/public_key.pem")


def verify_file(file_path, signature_path):

    file_path = Path(file_path)
    signature_path = Path(signature_path)

    if not file_path.exists():
        print("❌ File not found.")
        return

    if not signature_path.exists():
        print("❌ Signature file not found.")
        return

    # Load public key
    public_key = serialization.load_pem_public_key(
        PUBLIC_KEY.read_bytes()
    )

    # Read file and signature
    file_data = file_path.read_bytes()
    signature = signature_path.read_bytes()

    try:

        public_key.verify(
            signature,
            file_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        print("===================================")
        print("          SIGNSECURE")
        print("===================================")
        print("✅ SIGNATURE VALID")
        print("✅ File integrity verified.")

    except InvalidSignature:

        print("===================================")
        print("          SIGNSECURE")
        print("===================================")
        print("❌ SIGNATURE INVALID")
        print("⚠️ File may have been modified.")


if __name__ == "__main__":

    if len(sys.argv) < 3:

        print("Usage:")
        print("python verify_signature.py <file> <signature>")

    else:

        verify_file(
            sys.argv[1],
            sys.argv[2]
        )
        