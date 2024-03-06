import customtkinter as ctk
from PIL import Image,UnidentifiedImageError
import tkinter as tk
import requests
from io import BytesIO
import random
import os 
import sys
from Pokemon import Pokemon
              
class InterfaceGrafica:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root = ctk.CTk()
        self.largura = self.root.winfo_screenwidth()
        self.altura = self.root.winfo_screenheight()
        self.root.title("Pokedex")
        self.root.geometry("500x700")

        self.index = random.randint(0,len(pokemon.imagem))
        self.adivinhado = False
        self.gerar_aleatorio = ctk.CTkButton(self.root,text="Next",font=("Roboto",12),width=170,command=lambda: self.pokemon_aleatorio())

        
        self.label_imagem = ctk.CTkLabel(self.root,text="")
        self.label_imagem.pack()
        
        self.frame_tipos = ctk.CTkFrame(self.root,width=100,height=50)
        self.frame_tipos.pack()
        self.labels_tipos = [ctk.CTkLabel(self.frame_tipos,text=""), ctk.CTkLabel(self.frame_tipos,text="")]

            
        self.label_id = ctk.CTkLabel(self.root,text="")
        self.label_id.pack()

        self.frame_info = ctk.CTkFrame(self.root)
        self.frame_info.pack(pady=20)
        path = f"{os.path.dirname(sys.argv[0])}/images/"
        icones = []
        self.icones_adv = []
        for type in os.listdir(path):
            if os.path.isfile(os.path.join(path, type)):
                icones.append(f"{os.path.dirname(sys.argv[0])}/images/{type}")
                
        for c in range(len(icones)):  
            icone = Image.open(icones[c])     
            icone = ctk.CTkImage(icone,size=(40,40))
            if c == 0 or c == 6 or c == 12:
                frame_icone = ctk.CTkFrame(self.frame_info)
                frame_icone.pack()
            label_icone = ctk.CTkLabel(frame_icone,text="",image=icone)
            label_icone.bind("<Button-1>", lambda event, icone = icones[c]:self.adicionar_tipo(icone,adicionar=True))
            label_icone.pack(side=ctk.LEFT)
                        
        self.frame_tipos_adv = ctk.CTkFrame(self.root,width=100,height=50)
        self.frame_tipos_adv.pack(pady=(0,20))
        
        self.botao_adivinhar = ctk.CTkButton(self.root,text="Guess the Types!",command=lambda:self.adivinhar())
        self.botao_adivinhar.pack()
        
        self.label_resposta = ctk.CTkLabel(self.root,text="",font=("Roboto",15))
        self.label_resposta.pack()
        self.best = 0
        self.streak = 0
        self.label_streak = ctk.CTkLabel(self.root,text=f"Streak: {self.streak}\nBest: {self.best}",font=("Roboto",15))
        self.label_streak.pack(pady=(0,10))
        
        self.mostrar_imagem()
        
    def adivinhar(self): 
        if self.adivinhado == False:
            if sorted(self.icones_adv) == sorted(self.tipos):
                self.label_resposta.configure(text="Correct!")
                self.streak += 1
                if self.streak > self.best:
                    self.best = self.streak
                self.label_streak.configure(text=f"Streak: {self.streak}\nBest: {self.best}")          
            elif sorted(self.icones_adv) != sorted(self.tipos):
                self.label_resposta.configure(text="Wrong.")
                if self.streak > self.best:
                    self.best = self.streak
                self.streak = 0
                self.label_streak.configure(text=f"Streak: {self.streak}\nBest: {self.best}")  
        for label_tipo in self.labels_tipos:
            label_tipo.pack(side=ctk.LEFT)
        self.gerar_aleatorio.pack()
        self.adivinhado = True
        
    def adicionar_tipo(self,icone,adicionar):
        
        #Adicionar tipo
        if len(self.icones_adv) <= 1 and adicionar == True:  
            icone_formatado = str(icone).split("images/")[1].split(" type.png")[0].lower()
            self.icones_adv.append(icone_formatado)
            icone = Image.open(icone)     
            icone = ctk.CTkImage(icone,size=(40,40))
            self.label_tipos_adv = ctk.CTkLabel(self.frame_tipos_adv,text="",image=icone)
            self.label_tipos_adv.bind("<Button-1>", lambda event, icone = icone_formatado:self.adicionar_tipo(icone,adicionar=False))
            self.label_tipos_adv.pack(side=ctk.LEFT)

        #Remover tipo
        if len(self.icones_adv) > 0 and adicionar == False:
            index = self.icones_adv.index(icone)
            self.icones_adv.pop(index)
            c = 0
            for widget in self.frame_tipos_adv.winfo_children():
                if c == index:
                    widget.destroy()
                c += 1
            
    def pokemon_aleatorio(self):
        self.index = random.randint(0,len(pokemon.imagem))
        self.adivinhado=False
        self.icones_adv = []
        for label_tipo in self.labels_tipos:
            label_tipo.pack_forget()
        for widget in self.frame_tipos_adv.winfo_children():
            widget.destroy()
        self.label_resposta.configure(text="")
        self.gerar_aleatorio.pack_forget()
        self.mostrar_imagem()

    def mostrar_imagem(self):
        base_url_formats = [
            "https://img.pokemondb.net/sprites/scarlet-violet/normal/{}.png",
            "https://img.pokemondb.net/sprites/home/normal/{}.png",
            "https://img.pokemondb.net/sprites/sun-moon/normal/{}.png",
            "https://img.pokemondb.net/sprites/sword-shield/normal/{}.png",
        ]
        
        image_url = None

        for url_format in base_url_formats:
            image_url = url_format.format(pokemon.imagem[self.index])

            try:
                response = requests.get(image_url)
                response.raise_for_status()

                try:
                    img = Image.open(BytesIO(response.content))
                    break  
                except UnidentifiedImageError:
                    pass

            except requests.exceptions.HTTPError as http_err:
                image_url = None

            except Exception as err:
                image_url = None
                
        img = ctk.CTkImage(img,size=(128,128))
        self.label_imagem.configure(image=img)
        self.label_id.configure(text="{} {}".format(pokemon.id[self.index], pokemon.nome[self.index])) 
        for label_tipo in self.labels_tipos:
            label_tipo.configure(image=None)
        
        self.tipos = pokemon.tipos[self.index].split('/')
        for i, tipo in enumerate(self.tipos):
            icone = self.carregar_icone(tipo)
            if icone:
                self.labels_tipos[i].configure(image=icone)
   
    
    def carregar_icone(self,tipo):
        icone_path = f"{os.path.dirname(sys.argv[0])}/images/{str(tipo).title()} type.png"
        icone = Image.open(icone_path)
        icone = ctk.CTkImage(icone,size=(30,30)) 
        return icone
    
    def iniciar(self):
        self.root.mainloop()

if __name__ == "__main__":
    pokemon = Pokemon()
    pokemon.coletar_dados() 
    app = InterfaceGrafica()
    app.iniciar()