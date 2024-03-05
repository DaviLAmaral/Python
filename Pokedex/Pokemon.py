import requests
from bs4 import BeautifulSoup

class Pokemon:
    def __init__(self):    
        self.imagem = []
        self.nome = []
        self.id = []
        self.stats = []
        self.tipos = []
        self.links = []
        self.hp = []
        self.atk = []
        self.deff = []
        self.spatk = []
        self.spdef = []
        self.speed = []
        self.indices = []
        self.abilities = []
        
    
    def coletar_dados(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'} 
        
        page ="https://pokemondb.net/pokedex/all"
        pageTree = requests.get(page, headers=headers)
        pageSoup = BeautifulSoup(pageTree.content, "html.parser")
        p = pageSoup.find_all("td")
        for pk in p:
            if "href=" in str(pk) and "type" not in str(pk):
                self.links.append("https://pokemondb.net{}".format(str(pk).split('" href="')[1].split('" title="',1)[0]))
                if "https://pokemondb.net{}".format(str(pk).split('" href="')[1].split('" title="',1)[0]) == "https://pokemondb.net/pokedex/pyukumuku":
                    self.links.append("https://pokemondb.net/pokedex/type-null")
            if "type" in str(pk) and len(str(pk).split("type-icon type-",1)) > 1 and len((str(pk).split("type-icon type-",1)[1])) < 60:
                self.tipos.append((str(pk).split("type-icon type-",1)[1]).split('" href')[0])
            elif "type" in str(pk) and len(str(pk).split("type-icon type-",1)) > 1 and len((str(pk).split("type-icon type-",1)[1])) > 60:
                self.tipos.append("{}/{}".format((str(pk).split("type-icon type-",1)[1]).split('" href')[0],str(pk).split("type-icon type-",1)[1].split("type-icon type-",1)[1].split('" href',1)[0]))
            
            if "num" in str(pk):
                pok = str(pk).split('num">',1)
                if len(pok) >= 2:
                    self.stats.append(pok[1].split("</td>",1)[0])
            if "png" in str(pk):
                pkn = str(pk.find("img")).split('src="',1)[1].split('" width',1)[0]
                self.imagem.append(pkn.split("icon/")[1].split(".png")[0])

            if "alt" in str(pk):
                pk = str(pk).split('img alt="',1)
                if len(pk) >= 2:
                    self.nome.append(pk[1].split('" class=',1)[0])
            if "value" in str(pk):
                self.id.append(str(pk).split('value="',1)[1].split('"><span',1)[0].split('data">')[1].split("</span>")[0])

        for c in range(len(self.stats)):
            if c == 0 or c % 6 == 0:
                self.hp.append(self.stats[c])
            if c == 1 or c % 6 == 1:
                self.atk.append(self.stats[c])
            if c == 2 or c % 6 == 2:
                self.deff.append(self.stats[c])
            if c == 3 or c % 6 == 3:
                self.spatk.append(self.stats[c])
            if c == 4 or c % 6 == 4:
                self.spdef.append(self.stats[c])
            if c == 5 or c % 6 == 5:
                self.speed.append(self.stats[c])
    
    def coletar_detalhes(self,index):
        self.abilities = []
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        
        page = self.links[index]
        pageTree = requests.get(page, headers=headers)
        pageSoup = BeautifulSoup(pageTree.content, "html.parser")
        p = pageSoup.find_all("td")
        abilities = []
        for pk in p:
            if "ability" in str(pk):
                if "cell-med-text" not in str(pk):
                    abilities.append(str(pk).split('.">'))
        for a in abilities:
            allab = []
            if len(a) > 2:
                for i in range(1,len(a)):
                    if "hidden ability" in str(a[i]):
                        allab.append("{} (hidden ability)".format(str(a[i]).split("</a>")[0]))
                    else:
                        allab.append((str(a[i]).split("</a>")[0]))
                self.abilities.append(allab)
            if len(a) == 2:
                if "hidden ability" in str(a[1]):    
                    self.abilities.append("{} (hidden ability)".format(str(a[1]).split("</a>")[0]))
                else: 
                    self.abilities.append(str(a[1]).split("</a>")[0])
        

