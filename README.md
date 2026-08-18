# 🔐 SignSecure

## Digital Signature & File Integrity Verification System

SignSecure is a Python-based cybersecurity application designed to digitally sign files and verify their authenticity and integrity using public-key cryptography.

The project combines **RSA-3072**, **RSA-PSS**, and **SHA-256** to create and verify digital signatures. It provides a modern dark SOC-style cybersecurity dashboard for file hashing, digital signing, signature verification, tamper detection, key management, security logging, and security reporting.

> **SignSecure helps detect unauthorized modification of digitally signed files and provides a clear security result to the user.**

---

## 🛡️ Features

- 🔑 RSA-3072 key generation
- ✍️ Digital file signing
- 🔍 Digital signature verification
- #️⃣ SHA-256 file hashing
- 🚨 File tamper detection
- 📁 Multiple file support
- 🖥️ SOC-style dark cybersecurity GUI
- 📝 Security event logging
- 📊 Security metrics dashboard
- 📄 Security report generation
- 🔐 Public/private key management

---

## 🧠 How It Works

### Digital Signing

```text
File
 ↓
SHA-256
 ↓
RSA-3072 Private Key
 ↓
RSA-PSS
 ↓
Digital Signature
 ↓
file_name.sig
````

### Signature Verification

```text
Current File
     +
Signature
     +
Public Key
     ↓
RSA-PSS Verification
     ↓
  ┌───┴────┐
  ▼        ▼
VALID    INVALID
  │        │
  ▼        ▼
✅ SAFE   🚨 ALERT
           ❌ TAMPERING
```

---

## 🔐 Cryptography Used

| Component               | Technology            |
| ----------------------- | --------------------- |
| Public-Key Cryptography | RSA-3072              |
| Digital Signature       | RSA-PSS               |
| Hash Function           | SHA-256               |
| Key Format              | PEM                   |
| Cryptography Library    | Python `cryptography` |

### Private Key

The private key is used to create digital signatures.

```text
keys/private_key.pem
```

**Never upload or share the private key.**

### Public Key

The public key is used to verify digital signatures.

```text
keys/public_key.pem
```

The public key can be shared for verification.

---

## 🖥️ Application Modules

### 🏠 Dashboard

Displays:

* Files processed
* Signatures created
* Successful verifications
* Threats detected
* Security events

### 📁 File Integrity

Calculates the SHA-256 cryptographic hash of a selected file.

### ✍️ Digital Signing

Creates a digital signature using RSA-3072, RSA-PSS, and SHA-256.

### 🔍 Verification Center

Verifies a selected file against its digital signature and detects possible modification.

### #️⃣ Hash Analyzer

Generates SHA-256 hashes for file integrity analysis.

### 🔑 Key Management

Generates and manages the RSA public/private key pair.

### 📊 Security Reports

Generates security reports containing information about application activity and cryptographic operations.

---

## 📂 Project Structure

```text
SignSecure/
│
├── app.py
├── generate_keys.py
├── hash_utils.py
├── sign_file.py
├── verify_signature.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── keys/
│   ├── private_key.pem
│   └── public_key.pem
│
├── files/
│
├── signatures/
│
├── reports/
│
├── screenshots/
│
└── tests/
```

> ⚠️ `private_key.pem` must never be committed to GitHub.

---

## ⚙️ Requirements

* Python 3.13 or compatible Python 3 version
* CustomTkinter
* Cryptography
* Windows / Linux / macOS

### Dependencies

```text
customtkinter
cryptography
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Soumya-CSE/SignSecure.git
```

### 2. Enter the project directory

```bash
cd SignSecure
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

#### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Run the application

```bash
python app.py
```

---

## 🔑 First-Time Setup

Open SignSecure and go to the **Key Management** section.

Generate an RSA-3072 key pair.

The application creates:

```text
keys/private_key.pem
keys/public_key.pem
```

The private key is used for signing.

The public key is used for verification.

**Keep the private key secure.**

---

## ✍️ How to Sign a File

### Step 1

Open SignSecure.

### Step 2

Select a file.

Example:

```text
message.txt
```

### Step 3

Click:

```text
CREATE DIGITAL SIGNATURE
```

### Step 4

SignSecure performs:

```text
SHA-256
   ↓
RSA-3072 Private Key
   ↓
RSA-PSS
   ↓
Digital Signature
```

### Step 5

The signature is saved as:

```text
signatures/message.txt.sig
```

---

## 🔍 How to Verify a File

### Step 1

Select the signed file:

```text
message.txt
```

### Step 2

SignSecure loads:

```text
public_key.pem
```

and:

```text
message.txt.sig
```

### Step 3

Click:

```text
VERIFY DIGITAL SIGNATURE
```

### Valid Signature

```text
✅ SIGNATURE VALID
✅ FILE INTEGRITY VERIFIED
```

### Invalid Signature

```text
🚨 SECURITY ALERT
❌ SIGNATURE INVALID
⚠️ POSSIBLE FILE TAMPERING DETECTED
```

---

## 🧪 Tamper Detection Demonstration

Tamper detection is the main cybersecurity demonstration of SignSecure.

### Step 1 — Create a file

Create:

```text
message.txt
```

Example:

```text
Hello, this is the original file.
```

### Step 2 — Sign the file

Create:

```text
message.txt.sig
```

### Step 3 — Modify the file

Change the content to:

```text
Hello, this file has been modified.
```

Do not create a new signature.

### Step 4 — Verify

Click:

```text
VERIFY DIGITAL SIGNATURE
```

### Expected Result

```text
🚨 SECURITY ALERT

❌ SIGNATURE INVALID

⚠️ POSSIBLE FILE TAMPERING DETECTED
```

This demonstrates **file integrity verification** using digital signatures.

---

## 🔄 Complete Security Workflow

```text
                  ┌──────────────────┐
                  │    SELECT FILE   │
                  └────────┬─────────┘
                           ▼
                  ┌──────────────────┐
                  │     SHA-256      │
                  │  FILE HASHING    │
                  └────────┬─────────┘
                           ▼
                  ┌──────────────────┐
                  │     RSA-3072     │
                  │   PRIVATE KEY    │
                  └────────┬─────────┘
                           ▼
                  ┌──────────────────┐
                  │     RSA-PSS      │
                  │ DIGITAL SIGNATURE │
                  └────────┬─────────┘
                           ▼
                  ┌──────────────────┐
                  │     .SIG FILE    │
                  └────────┬─────────┘
                           ▼
                  ┌──────────────────┐
                  │    VERIFICATION  │
                  │    PUBLIC KEY    │
                  └────────┬─────────┘
                           │
                       ┌───┴────┐
                       ▼        ▼
                    ✅ VALID   🚨 INVALID
                       │        │
                       ▼        ▼
                  AUTHENTIC  TAMPERING
                  INTEGRITY  DETECTED
```

---

## 🧩 Technologies Used

```text
Python
CustomTkinter
Cryptography
RSA-3072
RSA-PSS
SHA-256
PEM
Git
GitHub
```

---

## 🎯 Cybersecurity Concepts Demonstrated

* Cryptographic hashing
* SHA-256
* Public-key cryptography
* RSA key pairs
* Digital signatures
* RSA-PSS
* File integrity verification
* Tamper detection
* Security event logging
* Security monitoring
* Security reporting
* Secure private-key handling

---

## 🔐 Why SHA-256?

SHA-256 creates a cryptographic fingerprint of a file.

```text
Original File
     ↓
   SHA-256
     ↓
  File Hash
```

Even a small change to the file results in a different cryptographic hash.

This makes hashing useful for detecting file modifications.

---

## 🔑 Why RSA?

RSA is an asymmetric cryptographic algorithm that uses two keys:

```text
PRIVATE KEY
    ↓
   SIGN
    ↓
DIGITAL SIGNATURE
    ↓
  VERIFY
    ↑
PUBLIC KEY
```

The private key remains secret while the public key can be shared.

---

## 🛡️ Why RSA-PSS?

RSA-PSS is a modern padding scheme for RSA digital signatures.

SignSecure combines:

```text
RSA-3072
   +
RSA-PSS
   +
SHA-256
```

to provide the digital signature mechanism.

---

## 🔐 Digital Signature vs Encryption

SignSecure primarily uses **digital signatures**, not encryption.

### Encryption

Purpose:

```text
CONFIDENTIALITY
```

Encryption prevents unauthorized users from reading protected data.

### Digital Signature

Purpose:

```text
AUTHENTICITY
+
INTEGRITY
```

Digital signatures help verify that signed data has not been modified and that the signature corresponds to the private key used for signing.

---

## 📝 Security Event Logging

SignSecure records security-related events such as:

```text
FILE SELECTED
HASH GENERATED
SIGNATURE CREATED
VERIFICATION SUCCESS
VERIFICATION FAILED
SECURITY ALERT
```

Example:

```text
[16:20:10] FILE SELECTED
[16:20:11] HASH GENERATED
[16:20:15] SIGNATURE CREATED
[16:20:21] VERIFICATION SUCCESS
[16:21:02] SECURITY ALERT
```

This provides a simple audit trail for application activity.

---

## 📊 Security Dashboard

The dashboard provides security metrics such as:

```text
FILES PROCESSED
SIGNATURES CREATED
VERIFIED FILES
THREATS DETECTED
```

This gives SignSecure a SOC-style security monitoring experience.

---

## 📸 Screenshots

### 🏠 Home Page 
<img width="1913" height="1014" alt="Home" src="https://github.com/user-attachments/assets/fa3faab5-80a6-419c-bf40-7c51507d78ee" />

### 📂 File Upload
<img width="1917" height="1011" alt="Upload File" src="https://github.com/user-attachments/assets/0906760e-ffa8-45ed-8d87-d3af4c9f9257" />

### 🛠️ Signatured Successfully 
<img width="1913" height="1013" alt="Signatured" src="https://github.com/user-attachments/assets/eced0e58-f4d6-4462-8202-394c9aaf0bb0" />


### ✅ Signature Validated Successfully
<img width="1919" height="1000" alt="Valided" src="https://github.com/user-attachments/assets/b33c4c8c-88d2-4b66-a862-b449a1133bfc" />

### ❌ Signature Verification Failed
<img width="1919" height="1014" alt="Invalided" src="https://github.com/user-attachments/assets/24edd014-7a62-419b-8a87-25062593ee1e" />

---

## ⚠️ Security Considerations

SignSecure is an educational and cybersecurity portfolio project.

A production-grade digital signature system would require additional controls such as:

* Trusted Public Key Infrastructure (PKI)
* Certificate Authorities
* Certificate validation
* Secure private-key storage
* Hardware Security Modules
* Hardware-backed key protection
* Key rotation
* Key revocation
* Trusted timestamping
* Centralized audit logging
* Authentication and authorization

### Important

Never commit:

```text
keys/private_key.pem
```

to GitHub.

Use the following `.gitignore`:

```gitignore
venv/
__pycache__/
*.pyc
keys/private_key.pem
signatures/*.sig
.env
```

---

## 🔮 Future Enhancements

* Database-backed audit logging
* Signature history
* Batch file signing
* Batch signature verification
* Certificate-based identities
* Digital certificate support
* PDF security reports
* Automated unit testing
* Role-based access control
* Hardware-backed key storage
* Certificate revocation checking
* Centralized SOC monitoring
* Multi-user support

---

## 💻 GitHub Repository

[https://github.com/Soumya-CSE/SignSecure](https://github.com/Soumya-CSE/SignSecure)

---

## 👨‍💻 Author

**Soumya Kanti Hazra**

Computer Science & Engineering

Aspiring SOC Analyst | Cybersecurity Enthusiast

GitHub:
[https://github.com/Soumya-CSE](https://github.com/Soumya-CSE)

---

## 📜 License

This project is intended for educational, learning, and cybersecurity portfolio purposes.

---

## ⭐ Project Summary

**SignSecure** demonstrates how digital signatures can be used to verify file authenticity and integrity.

The core security principle is:

```text
PRIVATE KEY
     ↓
   SIGN
     ↓
DIGITAL SIGNATURE
     ↓
  VERIFY
     ↑
PUBLIC KEY
```

> **SignSecure digitally signs files using an RSA private key and verifies them using the corresponding public key, allowing unauthorized file modifications to be detected.**

## ⭐ Support

If you found **SignSecure** useful for learning about **Digital Signatures, Cryptography, Cybersecurity, Python, or GUI Application Development**, consider giving the repository a ⭐ on GitHub.

Your support and feedback are greatly appreciated! 🙌🔐


