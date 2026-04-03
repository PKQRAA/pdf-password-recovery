import os
import sys
import itertools
import time
from datetime import datetime
from pypdf import PdfReader

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class Fore:
        RED = GREEN = YELLOW = CYAN = BLUE = ""
    class Style:
        RESET_ALL = BRIGHT = ""

class PDFPasswordRecovery:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.found_password = None
        self.attempts = 0
        self.start_time = None
        
        if not os.path.exists(pdf_path):
            print(f"{Fore.RED}✗ File not found: {pdf_path}{Style.RESET_ALL}")
            sys.exit(1)
    
    def try_password(self, password):
        self.attempts += 1
        
        if self.attempts % 100 == 0:
            elapsed = time.time() - self.start_time
            rate = self.attempts / elapsed if elapsed > 0 else 0
            print(f"{Fore.CYAN}Attempts: {self.attempts} | Rate: {rate:.0f}/s{Style.RESET_ALL}")
        
        try:
            reader = PdfReader(self.pdf_path)
            reader.decrypt(password)
            return True
        except:
            return False
    
    def dictionary_attack(self, wordlist_path):
        if not os.path.exists(wordlist_path):
            print(f"{Fore.RED}✗ Wordlist not found: {wordlist_path}{Style.RESET_ALL}")
            return False
        
        print(f"{Fore.YELLOW}📖 Dictionary Attack Started{Style.RESET_ALL}")
        print(f"Wordlist: {wordlist_path}\n")
        
        self.start_time = time.time()
        
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                password = line.strip()
                if not password:
                    continue
                
                if self.try_password(password):
                    self.found_password = password
                    self._success()
                    return True
                
                if self.attempts % 500 == 0:
                    print(f"  Trying: {password[:20]}...")
        
        print(f"\n{Fore.RED}✗ Password not found in wordlist{Style.RESET_ALL}")
        return False
    
    def brute_force(self, charset, max_length):
        print(f"{Fore.YELLOW}🔓 Brute Force Attack Started{Style.RESET_ALL}")
        print(f"Charset: {charset}")
        print(f"Max length: {max_length}\n")
        
        self.start_time = time.time()
        
        for length in range(1, max_length + 1):
            print(f"{Fore.CYAN}Testing length: {length}{Style.RESET_ALL}")
            
            for attempt in itertools.product(charset, repeat=length):
                password = ''.join(attempt)
                
                if self.try_password(password):
                    self.found_password = password
                    self._success()
                    return True
                
                if self.attempts % 10000 == 0:
                    elapsed = time.time() - self.start_time
                    rate = self.attempts / elapsed if elapsed > 0 else 0
                    print(f"  Progress: {self.attempts} attempts ({rate:.0f}/s)")
        
        print(f"\n{Fore.RED}✗ Password not found within given parameters{Style.RESET_ALL}")
        return False
    
    def _success(self):
        elapsed = time.time() - self.start_time
        print(f"\n{Fore.GREEN}✓ PASSWORD FOUND!{Style.RESET_ALL}")
        print(f"  Password: {self.found_password}")
        print(f"  Attempts: {self.attempts}")
        print(f"  Time: {elapsed:.2f}s")
        
        with open("recovered_password.txt", "w") as f:
            f.write(f"PDF: {self.pdf_path}\n")
            f.write(f"Password: {self.found_password}\n")
            f.write(f"Recovered: {datetime.now()}\n")
            f.write(f"Attempts: {self.attempts}\n")
        
        print(f"\n{Fore.GREEN}✓ Saved to recovered_password.txt{Style.RESET_ALL}")

def main():
    if len(sys.argv) < 2:
        print("""
╔════════════════════════════════════════╗
║     PDF Password Recovery Tool 🔓      ║
╠════════════════════════════════════════╣
║ Usage:                                  ║
║   python pdf_cracker.py file.pdf       ║
║                                         ║
║ Dictionary Attack:                      ║
║   python pdf_cracker.py file.pdf dict.txt║
║                                         ║
║ Brute Force:                            ║
║   python pdf_cracker.py file.pdf --brute --length 4 ║
╚════════════════════════════════════════╝
        """)
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    recovery = PDFPasswordRecovery(pdf_path)
    
    if len(sys.argv) > 2:
        if sys.argv[2] == "--brute":
            charset = "abcdefghijklmnopqrstuvwxyz0123456789"
            length = 4
            
            i = 2
            while i < len(sys.argv):
                if sys.argv[i] == "--charset" and i + 1 < len(sys.argv):
                    charset = sys.argv[i + 1]
                    i += 2
                elif sys.argv[i] == "--length" and i + 1 < len(sys.argv):
                    length = int(sys.argv[i + 1])
                    i += 2
                else:
                    i += 1
            
            recovery.brute_force(charset, length)
        
        elif not sys.argv[2].startswith("--"):
            wordlist_path = sys.argv[2]
            recovery.dictionary_attack(wordlist_path)
        else:
            print(f"{Fore.RED}Invalid arguments{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.YELLOW}No wordlist provided.{Style.RESET_ALL}")
        print(f"Create a wordlist or use --brute for brute force.")

if __name__ == "__main__":
    main()