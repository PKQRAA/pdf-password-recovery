# PDF Password Recovery 🔓

A tool to recover forgotten PDF passwords using dictionary attack.

## ⚠️ Legal Notice
**For recovery of YOUR OWN files only!** Unauthorized access to others' files is illegal.

## Features
- Dictionary-based password attack
- Character brute-force attack (configurable length)
- Progress tracking
- Resume capability

## Installation
```bash
pip install pypdf
```

## Usage
```bash
# Dictionary attack
python pdf_cracker.py file.pdf wordlist.txt

# Brute force (alphanumeric, max 4 chars)
python pdf_cracker.py file.pdf --brute --length 4

# Custom character set
python pdf_cracker.py file.pdf --brute --charset abc123 --length 3
```

## How it works
1. Loads PDF file
2. Attempts to decrypt using passwords from wordlist or generated combinations
3. Stops when correct password is found
4. Saves found password to `recovered_password.txt`