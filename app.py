import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
from datetime import datetime
import hashlib

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding


# ============================================================
# SIGNSECURE - CYBERSECURITY DIGITAL SIGNATURE CONSOLE
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

BASE_DIR = Path(__file__).resolve().parent
KEY_DIR = BASE_DIR / "keys"
SIGNATURE_DIR = BASE_DIR / "signatures"
REPORT_DIR = BASE_DIR / "reports"

KEY_DIR.mkdir(exist_ok=True)
SIGNATURE_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)


class SignSecureApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("SignSecure | Cybersecurity Console")
        self.geometry("1250x780")
        self.minsize(1050, 700)

        self.selected_file = None
        self.files_processed = 0
        self.signatures_created = 0
        self.verifications_success = 0
        self.threats_detected = 0

        self.build_sidebar()
        self.build_dashboard()

    # ========================================================
    # SIDEBAR
    # ========================================================

    def build_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=230,
            corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(
            self.sidebar,
            text="SIGNSECURE",
            font=("Arial", 23, "bold")
        ).pack(pady=(30, 3))

        ctk.CTkLabel(
            self.sidebar,
            text="CYBERSECURITY CONSOLE",
            text_color="#7f8c8d",
            font=("Arial", 9, "bold")
        ).pack(pady=(0, 28))

        self.nav_buttons = {}

        self.create_nav_button("Dashboard", self.show_dashboard)
        self.create_nav_button("File Integrity", self.show_file_integrity)
        self.create_nav_button("Digital Signing", self.show_signing)
        self.create_nav_button("Verification", self.show_verification)
        self.create_nav_button("Hash Analyzer", self.show_hash_analyzer)
        self.create_nav_button("Key Management", self.show_key_management)
        self.create_nav_button("Security Reports", self.show_reports)

        ctk.CTkFrame(
            self.sidebar,
            height=2,
            fg_color="#263238"
        ).pack(fill="x", padx=18, pady=20)

        ctk.CTkLabel(
            self.sidebar,
            text="SYSTEM STATUS",
            text_color="#7f8c8d",
            font=("Arial", 9, "bold")
        ).pack(side="bottom", pady=(0, 4))

        ctk.CTkLabel(
            self.sidebar,
            text="ONLINE",
            text_color="#00ff88",
            font=("Arial", 12, "bold")
        ).pack(side="bottom", pady=(0, 25))

    def create_nav_button(self, text, command):
        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            anchor="w",
            height=40,
            corner_radius=7,
            fg_color="transparent",
            hover_color="#1f2937",
            command=command
        )
        button.pack(padx=14, pady=3, fill="x")
        self.nav_buttons[text] = button

    # ========================================================
    # MAIN AREA
    # ========================================================

    def clear_main(self):
        if hasattr(self, "main"):
            self.main.destroy()

        self.main = ctk.CTkFrame(self, corner_radius=0)
        self.main.pack(side="left", fill="both", expand=True)

    def page_header(self, title, subtitle):
        header = ctk.CTkFrame(self.main, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(25, 10))

        ctk.CTkLabel(
            header,
            text=title,
            font=("Arial", 27, "bold")
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text="SYSTEM ONLINE",
            text_color="#00ff88",
            font=("Arial", 11, "bold")
        ).pack(side="right", pady=8)

        ctk.CTkLabel(
            self.main,
            text=subtitle,
            text_color="#8b949e",
            font=("Arial", 12)
        ).pack(anchor="w", padx=30)

    # ========================================================
    # DASHBOARD
    # ========================================================

    def build_dashboard(self):
        self.show_dashboard()

    def show_dashboard(self):
        self.clear_main()
        self.page_header(
            "Security Overview",
            "Digital signature, file integrity and cryptographic security console."
        )

        metrics = ctk.CTkFrame(self.main, fg_color="transparent")
        metrics.pack(fill="x", padx=30, pady=20)

        self.files_card = self.create_card(
            metrics, "FILES PROCESSED",
            str(self.files_processed), 0
        )
        self.signatures_card = self.create_card(
            metrics, "SIGNATURES",
            str(self.signatures_created), 1
        )
        self.valid_card = self.create_card(
            metrics, "VERIFIED",
            str(self.verifications_success), 2
        )
        self.threat_card = self.create_card(
            metrics, "THREATS",
            str(self.threats_detected), 3
        )

        panel = ctk.CTkFrame(self.main)
        panel.pack(fill="both", expand=True, padx=30, pady=10)

        ctk.CTkLabel(
            panel,
            text="SECURITY OPERATIONS",
            font=("Arial", 18, "bold")
        ).pack(anchor="w", padx=22, pady=(20, 5))

        ctk.CTkLabel(
            panel,
            text="Choose an operation from the console.",
            text_color="#8b949e"
        ).pack(anchor="w", padx=22)

        operations = ctk.CTkFrame(panel, fg_color="transparent")
        operations.pack(fill="x", padx=20, pady=25)

        self.operation_button(
            operations, "SELECT FILE",
            self.select_file, 0, 0
        )
        self.operation_button(
            operations, "CREATE SIGNATURE",
            self.sign_file, 1, 0
        )
        self.operation_button(
            operations, "VERIFY SIGNATURE",
            self.verify_file, 2, 0
        )

        ctk.CTkLabel(
            panel,
            text="SECURITY EVENT LOG",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", padx=22, pady=(12, 5))

        self.log_box = ctk.CTkTextbox(panel, height=170)
        self.log_box.pack(fill="x", padx=22, pady=(0, 20))

        self.log_event(
            "SYSTEM",
            "SignSecure console initialized"
        )

    def create_card(self, parent, title, value, column):
        parent.grid_columnconfigure(column, weight=1)

        card = ctk.CTkFrame(parent, height=105)
        card.grid(
            row=0,
            column=column,
            padx=6,
            sticky="nsew"
        )

        ctk.CTkLabel(
            card,
            text=title,
            text_color="#8b949e",
            font=("Arial", 10, "bold")
        ).pack(pady=(18, 4))

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 27, "bold")
        )
        value_label.pack()

        return value_label

    def operation_button(self, parent, text, command, column, row):
        parent.grid_columnconfigure(column, weight=1)

        button = ctk.CTkButton(
            parent,
            text=text,
            height=45,
            command=command
        )
        button.grid(
            row=row,
            column=column,
            padx=7,
            sticky="ew"
        )

    # ========================================================
    # FILE INTEGRITY
    # ========================================================

    def show_file_integrity(self):
        self.clear_main()
        self.page_header(
            "File Integrity",
            "Calculate and inspect cryptographic fingerprints of files."
        )

        panel = ctk.CTkFrame(self.main)
        panel.pack(fill="both", expand=True, padx=30, pady=20)

        self.integrity_file_label = ctk.CTkLabel(
            panel,
            text="No file selected",
            text_color="#8b949e"
        )
        self.integrity_file_label.pack(anchor="w", padx=25, pady=(25, 10))

        ctk.CTkButton(
            panel,
            text="SELECT FILE",
            command=self.select_file
        ).pack(anchor="w", padx=25)

        ctk.CTkLabel(
            panel,
            text="SHA-256",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", padx=25, pady=(25, 5))

        self.integrity_hash = ctk.CTkTextbox(panel, height=90)
        self.integrity_hash.pack(fill="x", padx=25)

        if self.selected_file:
            self.integrity_file_label.configure(
                text=str(self.selected_file)
            )
            self.display_hash_in(self.integrity_hash)

    # ========================================================
    # DIGITAL SIGNING
    # ========================================================

    def show_signing(self):
        self.clear_main()
        self.page_header(
            "Digital Signing",
            "Create RSA-3072 / RSA-PSS digital signatures using SHA-256."
        )

        panel = ctk.CTkFrame(self.main)
        panel.pack(fill="both", expand=True, padx=30, pady=20)

        self.sign_file_label = ctk.CTkLabel(
            panel,
            text="No file selected",
            text_color="#8b949e"
        )
        self.sign_file_label.pack(anchor="w", padx=25, pady=(25, 10))

        ctk.CTkButton(
            panel,
            text="SELECT FILE",
            command=self.select_file
        ).pack(anchor="w", padx=25)

        ctk.CTkButton(
            panel,
            text="CREATE DIGITAL SIGNATURE",
            height=45,
            command=self.sign_file
        ).pack(fill="x", padx=25, pady=25)

        ctk.CTkLabel(
            panel,
            text="Algorithm: RSA-3072 + RSA-PSS + SHA-256",
            text_color="#00d9ff"
        ).pack(anchor="w", padx=25)

    # ========================================================
    # VERIFICATION
    # ========================================================

    def show_verification(self):
        self.clear_main()
        self.page_header(
            "Verification Center",
            "Verify authenticity and detect unauthorized file modification."
        )

        panel = ctk.CTkFrame(self.main)
        panel.pack(fill="both", expand=True, padx=30, pady=20)

        self.verify_file_label = ctk.CTkLabel(
            panel,
            text="No file selected",
            text_color="#8b949e"
        )
        self.verify_file_label.pack(anchor="w", padx=25, pady=(25, 10))

        ctk.CTkButton(
            panel,
            text="SELECT FILE",
            command=self.select_file
        ).pack(anchor="w", padx=25)

        self.verify_result = ctk.CTkLabel(
            panel,
            text="READY FOR VERIFICATION",
            font=("Arial", 17, "bold"),
            text_color="#00d9ff"
        )
        self.verify_result.pack(pady=35)

        ctk.CTkButton(
            panel,
            text="VERIFY DIGITAL SIGNATURE",
            height=50,
            command=self.verify_file
        ).pack(fill="x", padx=25)

    # ========================================================
    # HASH ANALYZER
    # ========================================================

    def show_hash_analyzer(self):
        self.clear_main()
        self.page_header(
            "Hash Analyzer",
            "Generate SHA-256 hashes for files and inspect integrity fingerprints."
        )

        panel = ctk.CTkFrame(self.main)
        panel.pack(fill="both", expand=True, padx=30, pady=20)

        ctk.CTkButton(
            panel,
            text="SELECT FILE",
            command=self.select_file
        ).pack(anchor="w", padx=25, pady=25)

        self.analyzer_hash = ctk.CTkTextbox(panel, height=120)
        self.analyzer_hash.pack(fill="x", padx=25)

        if self.selected_file:
            self.display_hash_in(self.analyzer_hash)

    # ========================================================
    # KEY MANAGEMENT
    # ========================================================

    def show_key_management(self):
        self.clear_main()
        self.page_header(
            "Key Management",
            "Manage the RSA-3072 key pair used by SignSecure."
        )

        panel = ctk.CTkFrame(self.main)
        panel.pack(fill="both", expand=True, padx=30, pady=20)

        private_exists = (KEY_DIR / "private_key.pem").exists()
        public_exists = (KEY_DIR / "public_key.pem").exists()

        status = (
            f"Private Key: {'AVAILABLE' if private_exists else 'MISSING'}\n"
            f"Public Key:  {'AVAILABLE' if public_exists else 'MISSING'}"
        )

        ctk.CTkLabel(
            panel,
            text=status,
            justify="left",
            font=("Consolas", 14)
        ).pack(anchor="w", padx=25, pady=25)

        ctk.CTkButton(
            panel,
            text="GENERATE NEW RSA-3072 KEY PAIR",
            height=50,
            command=self.generate_keys
        ).pack(fill="x", padx=25)

        ctk.CTkLabel(
            panel,
            text="WARNING: Generating a new key pair invalidates signatures created with the old private key.",
            text_color="#ffb000",
            wraplength=850
        ).pack(anchor="w", padx=25, pady=20)

    # ========================================================
    # REPORTS
    # ========================================================

    def show_reports(self):
        self.clear_main()
        self.page_header(
            "Security Reports",
            "Generate a local audit report of SignSecure activity."
        )

        panel = ctk.CTkFrame(self.main)
        panel.pack(fill="both", expand=True, padx=30, pady=20)

        summary = (
            f"Files processed       : {self.files_processed}\n"
            f"Signatures created    : {self.signatures_created}\n"
            f"Successful verifies   : {self.verifications_success}\n"
            f"Threats detected      : {self.threats_detected}\n"
        )

        ctk.CTkLabel(
            panel,
            text=summary,
            justify="left",
            font=("Consolas", 14)
        ).pack(anchor="w", padx=25, pady=25)

        ctk.CTkButton(
            panel,
            text="GENERATE SECURITY REPORT",
            height=48,
            command=self.generate_report
        ).pack(fill="x", padx=25)

    # ========================================================
    # FILE SELECTION
    # ========================================================

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a file"
        )

        if not file_path:
            return

        self.selected_file = Path(file_path)
        self.files_processed += 1

        self.update_metric_cards()
        self.calculate_hash()

        name = self.selected_file.name

        if hasattr(self, "file_label"):
            self.file_label.configure(
                text=name,
                text_color="white"
            )

        if hasattr(self, "integrity_file_label"):
            self.integrity_file_label.configure(
                text=str(self.selected_file),
                text_color="white"
            )

        if hasattr(self, "sign_file_label"):
            self.sign_file_label.configure(
                text=str(self.selected_file),
                text_color="white"
            )

        if hasattr(self, "verify_file_label"):
            self.verify_file_label.configure(
                text=str(self.selected_file),
                text_color="white"
            )

        self.log_event("FILE SELECTED", name)

    # ========================================================
    # SHA-256
    # ========================================================

    def calculate_hash(self):
        if not self.selected_file:
            return

        sha256 = hashlib.sha256()

        try:
            with self.selected_file.open("rb") as file:
                while True:
                    chunk = file.read(1024 * 1024)
                    if not chunk:
                        break
                    sha256.update(chunk)

            hash_value = sha256.hexdigest()

            if hasattr(self, "hash_box"):
                self.set_textbox(self.hash_box, hash_value)

            if hasattr(self, "integrity_hash"):
                self.set_textbox(self.integrity_hash, hash_value)

            if hasattr(self, "analyzer_hash"):
                self.set_textbox(self.analyzer_hash, hash_value)

            self.log_event("HASH GENERATED", "SHA-256")

        except Exception as error:
            messagebox.showerror(
                "Hash Error",
                str(error)
            )

    def display_hash_in(self, textbox):
        if not self.selected_file:
            return

        sha256 = hashlib.sha256()

        with self.selected_file.open("rb") as file:
            while True:
                chunk = file.read(1024 * 1024)
                if not chunk:
                    break
                sha256.update(chunk)

        self.set_textbox(textbox, sha256.hexdigest())

    def set_textbox(self, textbox, text):
        textbox.delete("1.0", "end")
        textbox.insert("1.0", text)

    # ========================================================
    # KEY GENERATION
    # ========================================================

    def generate_keys(self):
        try:
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=3072
            )

            public_key = private_key.public_key()

            private_bytes = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )

            public_bytes = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

            (KEY_DIR / "private_key.pem").write_bytes(private_bytes)
            (KEY_DIR / "public_key.pem").write_bytes(public_bytes)

            self.log_event(
                "KEY PAIR GENERATED",
                "RSA-3072"
            )

            messagebox.showinfo(
                "Key Management",
                "RSA-3072 key pair generated successfully."
            )

            self.show_key_management()

        except Exception as error:
            messagebox.showerror(
                "Key Generation Error",
                str(error)
            )

    # ========================================================
    # DIGITAL SIGNATURE
    # ========================================================

    def sign_file(self):
        if not self.selected_file:
            messagebox.showwarning(
                "No File",
                "Please select a file first."
            )
            return

        private_key_path = KEY_DIR / "private_key.pem"

        if not private_key_path.exists():
            answer = messagebox.askyesno(
                "Private Key Missing",
                "No private key was found.\n\nGenerate an RSA-3072 key pair now?"
            )

            if answer:
                self.generate_keys()
            return

        try:
            private_key = serialization.load_pem_private_key(
                private_key_path.read_bytes(),
                password=None
            )

            file_data = self.selected_file.read_bytes()

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
                f"{self.selected_file.name}.sig"
            )

            signature_path.write_bytes(signature)

            self.signatures_created += 1
            self.update_metric_cards()

            self.log_event(
                "SIGNATURE CREATED",
                f"RSA-3072 / RSA-PSS / {self.selected_file.name}"
            )

            messagebox.showinfo(
                "Signature Created",
                "Digital signature created successfully.\n\n"
                f"File: {self.selected_file.name}\n"
                f"Signature: {signature_path.name}"
            )

        except Exception as error:
            self.log_event(
                "SIGNING ERROR",
                str(error)
            )

            messagebox.showerror(
                "Signing Error",
                f"{type(error).__name__}\n\n{error}"
            )

    # ========================================================
    # DIGITAL SIGNATURE VERIFICATION
    # ========================================================

    def verify_file(self):
        if not self.selected_file:
            messagebox.showwarning(
                "No File Selected",
                "Please select a file first."
            )
            return

        public_key_path = KEY_DIR / "public_key.pem"
        signature_path = (
            SIGNATURE_DIR /
            f"{self.selected_file.name}.sig"
        )

        if not public_key_path.exists():
            messagebox.showerror(
                "Public Key Missing",
                "public_key.pem was not found."
            )
            return

        if not signature_path.exists():
            messagebox.showerror(
                "Signature Missing",
                f"No signature was found for:\n\n"
                f"{self.selected_file.name}\n\n"
                f"Expected:\n{signature_path.name}"
            )

            self.log_event(
                "VERIFICATION FAILED",
                "Signature file not found"
            )
            return

        try:
            public_key = serialization.load_pem_public_key(
                public_key_path.read_bytes()
            )

            file_data = self.selected_file.read_bytes()
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

            self.verifications_success += 1
            self.update_metric_cards()

            if hasattr(self, "verify_result"):
                self.verify_result.configure(
                    text="AUTHENTIC - INTEGRITY VERIFIED",
                    text_color="#00ff88"
                )

            self.log_event(
                "VERIFICATION SUCCESS",
                f"{self.selected_file.name} - AUTHENTIC"
            )

            messagebox.showinfo(
                "Verification Result",
                "SIGNATURE VALID\n\n"
                "AUTHENTICITY: VERIFIED\n"
                "INTEGRITY: VERIFIED\n\n"
                "No unauthorized modification was detected."
            )

        except InvalidSignature:
            self.threats_detected += 1
            self.update_metric_cards()

            if hasattr(self, "verify_result"):
                self.verify_result.configure(
                    text="SECURITY ALERT - SIGNATURE INVALID",
                    text_color="#ff4444"
                )

            self.log_event(
                "SECURITY ALERT",
                f"{self.selected_file.name} - POSSIBLE TAMPERING"
            )

            messagebox.showerror(
                "SECURITY ALERT",
                "SIGNATURE INVALID\n\n"
                "POSSIBLE FILE TAMPERING DETECTED.\n\n"
                "The current file content does not match "
                "the digitally signed content."
            )

        except Exception as error:
            if hasattr(self, "verify_result"):
                self.verify_result.configure(
                    text="VERIFICATION ERROR",
                    text_color="#ff4444"
                )

            self.log_event(
                "VERIFICATION ERROR",
                f"{type(error).__name__}: {error}"
            )

            messagebox.showerror(
                "Verification Error",
                f"{type(error).__name__}\n\n{error}"
            )

    # ========================================================
    # REPORT
    # ========================================================

    def generate_report(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report = (
            "SIGNSECURE SECURITY REPORT\n"
            "===========================\n\n"
            f"Generated: {timestamp}\n\n"
            f"Files processed: {self.files_processed}\n"
            f"Signatures created: {self.signatures_created}\n"
            f"Successful verifications: {self.verifications_success}\n"
            f"Threats detected: {self.threats_detected}\n\n"
            "Cryptographic algorithms:\n"
            "- SHA-256\n"
            "- RSA-3072\n"
            "- RSA-PSS\n"
        )

        report_path = (
            REPORT_DIR /
            f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        report_path.write_text(
            report,
            encoding="utf-8"
        )

        self.log_event(
            "REPORT GENERATED",
            report_path.name
        )

        messagebox.showinfo(
            "Security Report",
            f"Report generated successfully:\n\n{report_path}"
        )

    # ========================================================
    # METRICS / LOG
    # ========================================================

    def update_metric_cards(self):
        if hasattr(self, "files_card"):
            self.files_card.configure(
                text=str(self.files_processed)
            )

        if hasattr(self, "signatures_card"):
            self.signatures_card.configure(
                text=str(self.signatures_created)
            )

        if hasattr(self, "valid_card"):
            self.valid_card.configure(
                text=str(self.verifications_success)
            )

        if hasattr(self, "threat_card"):
            self.threat_card.configure(
                text=str(self.threats_detected)
            )

    def log_event(self, event, details):
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{timestamp}] {event:<22} {details}\n"

        if hasattr(self, "log_box"):
            self.log_box.insert("end", line)
            self.log_box.see("end")

    # ========================================================
    # START
    # ========================================================


if __name__ == "__main__":
    app = SignSecureApp()
    app.mainloop()
    