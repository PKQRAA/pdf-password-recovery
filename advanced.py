import os
import sys
import subprocess

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class Fore:
        RED = GREEN = YELLOW = CYAN = ""
    class Style:
        RESET_ALL = BRIGHT = ""

def print_menu():
    print(f"""
╔════════════════════════════════════════════════╗
║      PDF Password Recovery - Multiple Methods  🔓  ║
╠════════════════════════════════════════════════╣
║  Method 1: Dictionary Attack (Built-in)       ║
║  Method 2: Brute Force (Built-in)              ║
║  Method 3: qpdf Decrypt (If you have password) ║
║  Method 4: Hash Extraction + Hashcat           ║
╚════════════════════════════════════════════════╝
""")

def check_qpdf():
    try:
        result = subprocess.run(['qpdf', '--version'], capture_output=True, text=True)
        return True
    except:
        return False

def check_hashcat():
    try:
        result = subprocess.run(['hashcat', '--version'], capture_output=True, text=True)
        return True
    except:
        return False

def method1_dictionary():
    print(f"\n{Fore.CYAN}📖 Dictionary Attack{Style.RESET_ALL}")
    pdf = input("PDF file: ")
    wordlist = input("Wordlist file: ")
    
    if not os.path.exists(pdf):
        print(f"{Fore.RED}✗ PDF not found{Style.RESET_ALL}")
        return
    
    if not os.path.exists(wordlist):
        print(f"{Fore.RED}✗ Wordlist not found{Style.RESET_ALL}")
        return
    
    print(f"{Fore.YELLOW}Starting dictionary attack...{Style.RESET_ALL}")
    os.system(f"python pdf_cracker.py {pdf} {wordlist}")

def method2_bruteforce():
    print(f"\n{Fore.CYAN}🔓 Brute Force Attack{Style.RESET_ALL}")
    pdf = input("PDF file: ")
    length = input("Max length (default 4): ") or "4"
    charset = input("Charset (default abc): ") or "abc"
    
    print(f"{Fore.YELLOW}Starting brute force...{Style.RESET_ALL}")
    os.system(f"python pdf_cracker.py {pdf} --brute --length {length} --charset {charset}")

def method3_qpdf():
    if not check_qpdf():
        print(f"{Fore.RED}✗ qpdf not installed{Style.RESET_ALL}")
        print("Install: choco install qpdf (Windows) or apt install qpdf (Linux)")
        return
    
    print(f"\n{Fore.YELLOW}🔑 qPDF Decrypt (Owner method){Style.RESET_ALL}")
    pdf = input("Protected PDF: ")
    password = input("Password: ")
    output = input("Output file: ")
    
    if not password:
        print(f"{Fore.RED}Password required for this method{Style.RESET_ALL}")
        return
    
    os.system(f'qpdf --decrypt --password="{password}" "{pdf}" "{output}"')
    print(f"{Fore.GREEN}✓ Done{Style.RESET_ALL}")

def method4_hashcat():
    if not check_hashcat():
        print(f"{Fore.RED}✗ hashcat not installed{Style.RESET_ALL}")
        print("Download: https://hashcat.net/hashcat/")
        return
    
    print(f"\n{Fore.YELLOW}⚡ Hashcat Method (Fastest){Style.RESET_ALL}")
    print("This requires pdf2john to extract hash first")
    print("1. Get pdf2john from: https://github.com/openwall/john")
    print("2. Extract: python pdf2john.py protected.pdf > hash.txt")
    print("3. Crack: hashcat -m 10400 hash.txt wordlist.txt")
    print("\nCommon hashcat modes for PDF:")
    print("  10400 - PDF MD5")
    print("  10500 - PDF SHA256")
    print("  10600 - PDF SHA512")

def main():
    print_menu()
    
    print("Select method (1-4): ")
    choice = input("> ")
    
    if choice == "1":
        method1_dictionary()
    elif choice == "2":
        method2_bruteforce()
    elif choice == "3":
        method3_qpdf()
    elif choice == "4":
        method4_hashcat()
    else:
        print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")

if __name__ == "__main__":
    main()