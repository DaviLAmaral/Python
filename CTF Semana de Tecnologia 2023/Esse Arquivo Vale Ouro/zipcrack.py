import zipfile
import os
import sys

path = f"{os.path.dirname(sys.argv[0])}"
def crack_password(password_list, obj):

    idx = 0
 
    with open(password_list, 'rb') as file:
        for line in file:
            for word in line.split():
                try:
                    idx += 1
                    obj.extractall(pwd=word)
                    print("Password found at line", idx)
                    print("Password is", word.decode())
                    return True
                except:
                    continue
    return False
 
 
password_list = f"{path}/passwordlist.txt"
 
zip_file = f"{path}/a.zip"
 
# ZipFile object initialised
obj = zipfile.ZipFile(zip_file)
 
# count of number of words present in file
cnt = len(list(open(password_list, "rb")))
 
print("There are total", cnt,
      "number of passwords to test")
if crack_password(password_list, obj) == False:
    print("Password not found in this file")