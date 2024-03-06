chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
senha = "OMQEMDUEQMEK"
resposta = str()
for l in senha:
    if l != " ":
        for char in chars:
            if l == char:
                ind = chars.index(char)
        if ind >= 13:
            resposta += chars[ind-13]
        else:
            resposta += chars[ind+13]
    else:
        resposta += " "
print(resposta)