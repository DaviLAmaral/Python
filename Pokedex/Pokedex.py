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
        self.root.geometry("500x750")
        self.index = 0
    
        self.label_busca = ctk.CTkLabel(self.root,text="Insert the Pokemon name:")
        self.label_busca.pack()
        self.entrada_busca = ctk.CTkEntry(self.root,width=170)
        self.entrada_busca.pack()
        self.botao_busca = ctk.CTkButton(self.root, text="Search",font=("Roboto",12),command=self.buscar_pokemon)
        self.botao_busca.pack(pady=(5,0))
        
        self.gerar_aleatorio = ctk.CTkButton(self.root,text="Generate Random Pokemon",font=("Roboto",12),width=170,command=lambda: self.pokemon_aleatorio())
        self.gerar_aleatorio.pack(pady=(10,0))
        self.label_busca_resultado = ctk.CTkLabel(self.root, text="")
        self.label_busca_resultado.pack()
        
        self.label_imagem = ctk.CTkLabel(self.root,text="")
        self.label_imagem.pack()
        
        self.frame_tipos = ctk.CTkFrame(self.root)
        self.frame_tipos.pack()
        self.labels_tipos = [ctk.CTkLabel(self.frame_tipos,text=""), ctk.CTkLabel(self.frame_tipos,text="")]
        for label_tipo in self.labels_tipos:
            label_tipo.pack(side=ctk.LEFT)
            
        self.label_id = ctk.CTkLabel(self.root,text="")
        self.label_id.pack()

        self.botao_anterior = ctk.CTkButton(self.root,text="Previous",command=lambda: self.trocar_indice(direcao="anterior"))
        self.botao_anterior.pack()
        self.botao_proximo = ctk.CTkButton(self.root,text="Next",command=lambda: self.trocar_indice(direcao="proximo"))
        self.botao_proximo.pack()
    
        self.frame_info = ctk.CTkFrame(self.root)
        self.frame_info.pack(pady=20)

        self.label_total = ctk.CTkLabel(self.frame_info)
        self.label_total.pack()
        
        self.label_stats = ctk.CTkLabel(self.frame_info)
        self.label_stats.pack(side=ctk.LEFT,pady=(20,0))

        self.canvas_barras = tk.Canvas(self.frame_info,highlightthickness=0,bg="black", width=200, height=255)
        
        self.lista_resultados = tk.Listbox(self.frame_info,width=25,height=50,bg="black",highlightcolor="white",highlightthickness=0,fg="white")
        
        self.mostrar_imagem()
        
    def pokemon_aleatorio(self):
        self.index = random.randint(0,len(pokemon.imagem))
        self.mostrar_imagem()

    def buscar_pokemon(self):
        nome_pesquisado = self.entrada_busca.get().lower()
        resultados = []
        pokemon.indices.clear()
        for index, nome in enumerate(pokemon.nome):
            if nome_pesquisado in nome.lower():
                resultados.append(index)
                pokemon.indices.append(index)
        #Se não tem correspondências:
        if len(resultados) == 0:
            self.label_busca_resultado.configure(text="No results for this search.")
        #Se tem apenas uma correspondência:
        elif len(resultados) == 1:
            self.index = resultados[0]
            self.mostrar_imagem()
            self.label_busca_resultado.configure(text="")
        #Mais de uma correspondência
        else:
            self.label_busca_resultado.configure(text="Multiple Pokémon encountered. Choose one:")
            self.lista_resultados.delete(0, tk.END)
            for index in resultados:
                self.lista_resultados.insert(tk.END, "{} {}".format(pokemon.id[index], pokemon.nome[index]))
            self.lista_resultados.pack(pady=(60,70),padx=(0,20))
            self.lista_resultados.bind("<<ListboxSelect>>", self.atualizar_pokemon)
    
    def atualizar_pokemon(self,event):
        selecionado = self.lista_resultados.curselection()
        if selecionado:
            index_na_lista_original = int(selecionado[0])
            self.index = pokemon.indices[index_na_lista_original]
            self.mostrar_imagem()
            self.label_busca_resultado.configure(text="")

    def trocar_indice(self,direcao):
        if direcao == "anterior" and self.index > 0:
            self.index -= 1
        elif direcao == "proximo" and self.index < len(pokemon.imagem)-1:
            self.index += 1
        elif direcao == "anterior" and self.index == 0:
            self.index = len(pokemon.imagem)-1
        else:
            self.index = 0
        self.mostrar_imagem()
    
    def desenhar_barras(self):

        # Limpe o Canvas antes de desenhar novas barras
        self.canvas_barras.delete("all")

        # Valores de HP, Attack, Defense, Special Attack, Special Defense e Speed
        valores = [int(pokemon.hp[self.index]), int(pokemon.atk[self.index]), int(pokemon.deff[self.index]),
                int(pokemon.spatk[self.index]), int(pokemon.spdef[self.index]), int(pokemon.speed[self.index])]

        nomes_stats = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']

        x1, y1 = 10, 18
        espaco_entre_barras = 40

        for i, valor in enumerate(valores):
            # Calcula a largura da barra proporcional ao valor máximo (255 é o valor máximo para as estatísticas)
            largura_barra = (valor / 255) * 180

            # Desenha o retângulo da barra
            if valor < 30:
                self.canvas_barras.create_rectangle(x1, y1, x1 + largura_barra, y1 + 20, fill='red')
                self.canvas_barras.create_text(x1 - 10, y1 + 10, anchor='e', text=nomes_stats[i])
            elif valor < 60:
                self.canvas_barras.create_rectangle(x1, y1, x1 + largura_barra, y1 + 20, fill='orange')
                self.canvas_barras.create_text(x1 - 10, y1 + 10, anchor='e', text=nomes_stats[i])
            elif valor < 90:
                self.canvas_barras.create_rectangle(x1, y1, x1 + largura_barra, y1 + 20, fill='yellow')
                self.canvas_barras.create_text(x1 - 10, y1 + 10, anchor='e', text=nomes_stats[i])
            elif valor < 120:
                self.canvas_barras.create_rectangle(x1, y1, x1 + largura_barra, y1 + 20, fill='lime')
                self.canvas_barras.create_text(x1 - 10, y1 + 10, anchor='e', text=nomes_stats[i])
            else:
                self.canvas_barras.create_rectangle(x1, y1, x1 + largura_barra, y1 + 20, fill='green')
                self.canvas_barras.create_text(x1 - 10, y1 + 10, anchor='e', text=nomes_stats[i])
                        
            # Atualize as coordenadas para a próxima barra
            y1 += espaco_entre_barras

    def mostrar_imagem(self):
        pokemon.coletar_detalhes(self.index)
        self.label_total.configure(text="Total Stats: {}".format(int(pokemon.hp[self.index]) + int(pokemon.atk[self.index]) + int(pokemon.deff[self.index]) + int(pokemon.spatk[self.index]) + int(pokemon.spdef[self.index]) + int(pokemon.speed[self.index])))
        self.label_stats.configure(text="HP: {}\n\nAttack: {}\n\nDefense: {}\n\nSp.Attack: {}\n\nSp.Defense: {}\n\nSpeed: {}\n\n".format(pokemon.hp[self.index], pokemon.atk[self.index], pokemon.deff[self.index], pokemon.spatk[self.index], pokemon.spdef[self.index], pokemon.speed[self.index]))
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
                
        self.canvas_barras.pack(side=ctk.LEFT,padx=(25,25),pady=(15,30))
        img = ctk.CTkImage(img,size=(128,128))
        self.label_imagem.configure(image=img)
        n = 0 
        if pokemon.id[self.index] == pokemon.id[self.index-1] and len(pokemon.abilities) > 1:
            if pokemon.id[self.index-1] == pokemon.id[self.index-2]:
                if pokemon.id[self.index-2] == pokemon.id[self.index-3]:
                    n = 3
                else: 
                    n = 2
            else:     
                n = 1
        if len(pokemon.abilities[n]) < 4:
            abl = list(ability for ability in pokemon.abilities[n])
            abl = '\n'.join(abl)
        else:
            abl = pokemon.abilities[n]
        self.label_id.configure(text="{} {}\n\n{}\n".format(pokemon.id[self.index], pokemon.nome[self.index], abl)) 
        for label_tipo in self.labels_tipos:
            label_tipo.configure(image=None)
        
        tipos = pokemon.tipos[self.index].split('/')
        for i, tipo in enumerate(tipos):
            icone = self.carregar_icone(tipo)
            if icone:
                self.labels_tipos[i].configure(image=icone)
        self.desenhar_barras()     
    
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