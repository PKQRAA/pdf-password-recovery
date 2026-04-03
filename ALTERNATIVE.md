# PDF Password Recovery - Advanced Methods 🔓

Alternative methods for PDF password recovery when owner forgets password.

## Installation
```bash
pip install pypdf
```

## Method 1: Using PDF2john (Hash Extraction)
Extract password hash and use hashcat/john for faster cracking:

### Step 1: Install required tools
```bash
# On Linux/WSL - Install pdf2john
apt-get install pdf2john  # or download from john repo
```

### Step 2: Extract hash
```bash
pdf2john.pl protected.pdf > hash.txt
```

### Step 3: Crack with hashcat
```bash
# MD5
hashcat -m 10400 hash.txt wordlist.txt

# SHA256  
hashcat -m 10500 hash.txt wordlist.txt
```

---

## Method 2: Using qpdf (For Owner)
If you have the original PDF without encryption but lost password:

```bash
# Install qpdf
# Windows: choco install qpdf
# Linux: apt install qpdf

qpdf --decrypt --password=YOUR_PASSWORD input.pdf output.pdf
```

---

## Method 3: Python Script - Rainbow Table
```python
# For common passwords - generate rainbow table
python rainbow_attack.py
```

---

## Method 4: PDFtk (Owner Only)
```bash
# Install
# Windows: choco install pdftk
# Linux: apt install pdftk

pdftk protected.pdf input_pw YOUR_PASSWORD dump_data output decrypted.pdf
```