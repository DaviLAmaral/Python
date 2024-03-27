import pikepdf
from tqdm import tqdm
import os
import sys
path = f"{os.path.dirname(sys.argv[0])}"

# load password list
passwords = [ line.strip() for line in open(f"{path}/wordlist.txt") ]

# iterate over passwords
for password in tqdm(passwords, "Decrypting PDF"):
    try:
        # open PDF file
        with pikepdf.open(f"{path}/protegido.pdf", password=password) as pdf:
            # Password decrypted successfully, break out of the loop
            print(" Password found:", password)
            break
    except pikepdf._core.PasswordError as e:
        # wrong password, just continue in the loop
        continue