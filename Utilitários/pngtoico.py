from PIL import Image
import customtkinter as ctk

class InterfaceGrafica:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root = ctk.CTk()
        self.root.geometry("400x400")
        self.largura = self.root.winfo_screenwidth()
        self.altura = self.root.winfo_screenheight()
        self.root.title("Conversor de Arquivos")
        frame_principal = ctk.CTkFrame(self.root)
        frame_principal.pack(expand=True)
        frame_esquerda = ctk.CTkFrame(frame_principal)
        frame_esquerda.pack(fill="both")
        frame_direita = ctk.CTkFrame(frame_principal)
        frame_direita.pack(fill="both")
        
        label_arquivo = ctk.CTkLabel(frame_esquerda,text="Selecione o arquivo de imagem\n para modificar a extensão abaixo:")
        label_arquivo.pack(pady=(20,10),padx=20)
        self.botao_selecionar_arquivo = ctk.CTkButton(frame_esquerda,text="Selecionar Arquivo",command=self.selecionar_arquivo)
        self.botao_selecionar_arquivo.pack(pady=(0,20))
        label_formato = ctk.CTkLabel(frame_direita,text="Selecione o novo formato\n desejado abaixo:")
        label_formato.pack(pady=(0,10))
        self.menu_selecionar_novo_formato = ctk.CTkOptionMenu(frame_direita,values=["png","jpg","gif","ico","bmp","tiff","webp"])
        self.menu_selecionar_novo_formato.pack(pady=(0,35))
        botao_confirmar = ctk.CTkButton(frame_direita,text="Confirmar",command=self.confirmar)
        botao_confirmar.pack(side=ctk.BOTTOM,pady=(0,20))
        self.label_confirmacao = ctk.CTkLabel(frame_direita,text="")
        self.label_confirmacao.pack()    
    
    def selecionar_arquivo(self):
        self.arquivo_inicial = ctk.filedialog.askopenfilename()
    
    def confirmar(self):
        try:
            self.arquivo_aberto = Image.open(self.arquivo_inicial)
            print("{}.{}".format(self.arquivo_inicial.split(".")[0],self.menu_selecionar_novo_formato.get()))
            self.arquivo_aberto.save("{}.{}".format(self.arquivo_inicial.split(".")[0],self.menu_selecionar_novo_formato.get()),format=f"{self.menu_selecionar_novo_formato.get()}")        
            self.label_confirmacao.configure(text=f"Novo formato criado com sucesso.")    
        except Exception:
            self.label_confirmacao.configure(text=f"Erro ao abrir arquivo.")
    def iniciar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = InterfaceGrafica()
    app.iniciar()
