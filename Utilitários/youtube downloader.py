from pytube import YouTube, Playlist
import customtkinter as ctk

def checar():
    if checkbox.get() == 1:
        novideo = True
    else:
        novideo = False
    return novideo

def baixar(video,novideo):
    if novideo:
        video = video.streams.get_audio_only()
    else:
        video = video.streams.get_highest_resolution()
    video.download()
    label_resultado.configure(text="Downloaded Succesfully")
    
    
def executar(entrada, tipo):
    try:
        if tipo == "Playlist":
            videos = Playlist(entrada)
            for video in videos:
                video = YouTube(video)
                baixar(video,novideo=checar())
        else:
            video = YouTube(entrada)
            baixar(video,novideo=checar())
    except Exception:
        label_resultado.configure(text="Invalid URL")
        
root = ctk.CTk()
root.geometry("500x500")

label_principal = ctk.CTkLabel(root,text="Youtube Downloader",font=("Roboto",24))
label_principal.pack(pady=(20,0))

label_video = ctk.CTkLabel(root,text="Insert Video URL:",font=("Roboto",20))
label_video.pack(pady=(20,10))
entrada_video = ctk.CTkEntry(root)
entrada_video.pack()
botao_video = ctk.CTkButton(root,text="Download Video",command=lambda: executar(entrada=entrada_video.get(),tipo="Video"))
botao_video.pack()

label_playlist = ctk.CTkLabel(root,text="Insert Playlist URL:",font=("Roboto",20))
label_playlist.pack(pady=(40,10))
entrada_playlist = ctk.CTkEntry(root)
entrada_playlist.pack()
botao_playlist = ctk.CTkButton(root,text="Download Playlist",command=lambda: executar(entrada=entrada_playlist.get(),tipo="Playlist"))
botao_playlist.pack()

checkbox = ctk.CTkCheckBox(root,text="Audio Only")
checkbox.pack()

label_resultado = ctk.CTkLabel(root,text="")
label_resultado.pack()
root.mainloop()

