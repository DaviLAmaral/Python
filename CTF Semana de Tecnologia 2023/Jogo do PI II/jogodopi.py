import os
import sys

def find_incorrect_number(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    numeros = []
    npi = 2
    for line in lines:
        words = line.split()
        for word in words:
            if word.isnumeric():
                numeros.append(word)
            if word == "PI":
                if len(numeros) != npi:
                    print(numeros[int(len(numeros)/2)-1])
                    quit()
                else:
                    numeros = []
                npi += 1

    return 

if __name__ == "__main__":
    path = f"{os.path.dirname(sys.argv[0])}"
    filename = f"{path}/numeros.txt"  
    result = find_incorrect_number(filename)
    print(result)
