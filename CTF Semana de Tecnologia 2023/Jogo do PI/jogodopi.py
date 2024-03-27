import os
import sys
def find_incorrect_number(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    for line in lines:
        words = line.split()
        for word in words:
            if word.isnumeric() == True and int(word)%7 == 0:
                print("O Número incorreto é:",word)
                quit()
    return 

if __name__ == "__main__":
    filename = f"{os.path.dirname(sys.argv[0])}/pi.txt"
    print(filename)
    result = find_incorrect_number(filename)
    print(result)