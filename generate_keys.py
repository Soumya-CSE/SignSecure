from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from pathlib import Path


KEY_DIR = Path("keys")
KEY_DIR.mkdir(exist_ok=True)


# Generate RSA private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=3072
)

# Generate public key
public_key = private_key.public_key()


# Save private key
private_key_data = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

(KEY_DIR / "private_key.pem").write_bytes(private_key_data)


# Save public key
public_key_data = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

(KEY_DIR / "public_key.pem").write_bytes(public_key_data)


print("===================================")
print("       SIGNSECURE KEY GENERATOR")
print("===================================")
print("✅ RSA-3072 key pair generated!")
print()
print("Private Key : keys/private_key.pem")
print("Public Key  : keys/public_key.pem")
