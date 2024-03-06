import requests
from bs4 import BeautifulSoup
import pandas as pd
from itertools import zip_longest
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from io import BytesIO
from tkinter import filedialog

Allpos = ["Goalkeeper","Left-Back","Defender","Centre-Back","Right-Back","Defensive Midfield","Central Midfield","Left Midfield","Right Midfield","Attacking Midfield","Left Winger","Mittelfeld","Right Winger","Second Striker","Striker","Centre-Forward"]

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
}
continents = {
    "Europe": "https://www.transfermarkt.co.uk/wettbewerbe/europa?page=",
    "America": "https://www.transfermarkt.co.uk/wettbewerbe/amerika?page=",
    "Asia": "https://www.transfermarkt.co.uk/wettbewerbe/asien?page=",
    "Africa": "https://www.transfermarkt.co.uk/wettbewerbe/afrika?page="
}
optcontinents = {"Europe":12,"America":7,"Asia":6,"Africa":2}
Regionsl = {"Europe":0,"America":0,"Asia":0,"Africa":0}
r = ctk.CTk()
r.geometry('500x300')
checkboxes = {} 
aditional_option = {}
label_region_select = ctk.CTkLabel(r, text="Select the leagues to show:", font=("Roboto", 23))
label_region_select.pack(pady=30)

def select_region(continent):
    if checkboxes[continent].get() == 1:
        Regionsl[continent] = 2
    else:
        Regionsl[continent] = 0
def select_option(continent):
    if aditional_option[continent].get() == 1 and checkboxes[continent].get() == 1:
        Regionsl[continent] = optcontinents[continent]
    elif checkboxes[continent].get() == 1:
        Regionsl[continent] = 2      

def generate():
    websitesL = []
    imglinks = []
    flaglinks = []
    flagnames = []
    leaguenames = []
    for continent in continents:
        for c in range(1,Regionsl[continent]):
            pageL = continents[continent]+str(c)
            pageTreeL = requests.get(pageL, headers=headers)
            pageSoupL = BeautifulSoup(pageTreeL.content, "html.parser")
            leagues = pageSoupL.find_all("td")
            
            for league in leagues:
                link = league.find("a")
                if link and "startseite" in str(link) and "+" not in str(link):
                    websiteL = "https://www.transfermarkt.co.uk" + link["href"]
                    if websiteL not in websitesL:
                        websitesL.append(websiteL)
                img = league.find("img")
                if "png" in str(img) and "logo" not in str(img) and "discussion" not in str(img):
                    flaglink = img["src"]            
                    flaglinks.append(flaglink)
                    flagname = img["title"]
                    flagnames.append(flagname)
                if "png" in str(img) and "flagge" not in str(img) and "discussion" not in str(img):
                    imglink = img["src"]
                    leaguename = img["title"]
                    if imglink not in imglinks:
                        leaguenames.append(leaguename)
                        imglinks.append(imglink)
    root = ctk.CTkToplevel()
    app = ImageApp(root, imglinks, flaglinks, leaguenames, flagnames, websitesL)
    root.mainloop()

for continent in continents:
    option_menu = ctk.CTkFrame(r)
    option_menu.pack()
    
    checkboxes[continent] = ctk.CTkCheckBox(option_menu, text=continent, command=lambda c=continent: select_region(c))
    checkboxes[continent].pack(side=ctk.LEFT)
    
    aditional_option[continent] = ctk.CTkSwitch(option_menu, text="Top 20 (Recommended)/All",command=lambda c=continent:select_option(c))
    aditional_option[continent].pack(side=ctk.RIGHT)
    
class ImageApp:
    def __init__(self, root, imglinks, flaglinks, leaguenames, flagnames,websitesL):
        self.root = root
        self.root.title("Transfermarkt Leagues")

        self.img_links = imglinks
        self.flag_links = flaglinks
        self.league_names = leaguenames
        self.flag_names = flagnames
        self.league_links = websitesL

        self.current_img_index = 0
        self.current_flag_index = 0
        self.current_league_index = 0
        
        self.image_label_flag = ctk.CTkLabel(root, text="")
        self.image_label_flag.pack(side=tk.RIGHT)

        self.image_label_img = ctk.CTkLabel(root, text="")
        self.image_label_img.pack(side=tk.RIGHT)

        self.league_name_label = ctk.CTkLabel(root, text="")
        self.league_name_label.pack(side=tk.RIGHT)

        self.flag_name_label = ctk.CTkLabel(root, text="")
        self.flag_name_label.pack(side=tk.RIGHT)

        self.prev_button = ctk.CTkButton(root, text="Previous", command=self.show_prev_image)
        self.prev_button.pack()

        self.next_button = ctk.CTkButton(root, text="Next", command=self.show_next_image)
        self.next_button.pack()

        botao_salvar = ctk.CTkButton(root, text="Save Excel File To...", command=self.salvar_arquivo)
        botao_salvar.pack()

        self.show_images()

    def salvar_arquivo(self):
        self.caminho_arquivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel","*.xlsx"), ("Todos os Arquivos", "*.*")])

    def show_images(self):
        image_url = self.img_links[self.current_img_index]
        flag_url = self.flag_links[self.current_flag_index]
        league_name = self.league_names[self.current_img_index]
        flag_name = self.flag_names[self.current_flag_index]
        league_url = self.league_links[self.current_league_index]

        self.league_button = ctk.CTkButton(self.root,text="Generate " + league_name, command=self.open_link)
        self.league_button.pack()

        response_img = requests.get(image_url)
        image_data = BytesIO(response_img.content)
        image = Image.open(image_data)
        photo_img = ctk.CTkImage(image)
        self.image_label_img.configure(image=photo_img)
        self.image_label_img.image = photo_img

        response_flag = requests.get(flag_url)
        flag_data = BytesIO(response_flag.content)
        flag = Image.open(flag_data)
        photo_flag = ctk.CTkImage(flag)
        self.image_label_flag.configure(image=photo_flag)
        self.image_label_flag.image = photo_flag

        self.league_name_label.configure(text=f" {league_name} ")
        self.flag_name_label.configure(text=f" {flag_name} ")

    def show_prev_image(self):
        if self.current_img_index != 0:
            self.current_img_index = (self.current_img_index - 1)
            self.current_flag_index = (self.current_flag_index - 1)
            self.current_league_index = (self.current_league_index - 1)
        else:
            self.current_img_index = (len(self.img_links) -1)
            self.current_flag_index = (len(self.flag_links) -1)
            self.current_league_index = (len(self.league_links) -1)
        self.destroy_league_button() 
        self.show_images()

    def show_next_image(self):
        if self.current_img_index != len(self.img_links)-1:
            self.current_img_index = (self.current_img_index + 1)
            self.current_flag_index = (self.current_flag_index + 1) 
            self.current_league_index = (self.current_league_index + 1)
        else: 
            self.current_img_index = 0
            self.current_flag_index = 0
            self.current_league_index = 0
        self.destroy_league_button() 
        self.show_images()

    def destroy_league_button(self):
        if hasattr(self, 'league_button'):
            self.league_button.destroy()

    def open_link(self):
        pageT = str(self.league_links[self.current_league_index]) 
        pageTreeT = requests.get(pageT, headers=headers)
        pageSoupT = BeautifulSoup(pageTreeT.content, "html.parser")
        clubs = pageSoupT.find_all("td", {"class": "hauptlink no-border-links"})
        ClubsList = []
        for club in clubs:
            club_name = club.text.strip()
            ClubsList.append(club_name)
        websites = []
        for club in clubs:
            link = club.find("a")["href"]
            website = "https://www.transfermarkt.co.uk" + link
            websites.append(website)

        PlayersList = []
        AgeList = []
        PositionsList = []
        NationList = []
        ValuesList = []
        ClubList = []
        cleaned_values = []
        for c in range(len(websites)):
            print(f"Scraping {club_name} - {c+1}º")
            page = websites[c]
            pageTree = requests.get(page, headers=headers)
            pageSoup = BeautifulSoup(pageTree.content, "html.parser")
            club_name = ClubsList[c]

            Players = pageSoup.find_all("img", {"class": "bilderrahmen-fixed"})
            Age = pageSoup.find_all("td", {"class": "zentriert"})
            Positions = pageSoup.find_all("td")
            Nationality = pageSoup.find_all("td", {"class": "zentriert"})
            Values = pageSoup.find_all("td", {"class": "rechts hauptlink"})
            for i in range(0, len(Players)):
                PlayersList.append(str(Players[i]).split('" class', 1)[0].split('<img alt="', 1)[1])
                ClubList.append(club_name)

            for i in range(1, (len(Players) * 3), 3):
                if str(Age[i]).split("(", 1)[1].split(")", 1)[0].isnumeric():
                    AgeList.append(int(str(Age[i]).split("(", 1)[1].split(")", 1)[0]))

            for i in range(1, len(Positions),2):
                ifpos = any(pos in str(Positions[i]) for pos in Allpos)
                if ifpos:
                    position = str(Positions[i]).replace("\n","").replace("<td>","").replace("</td>","").lstrip()
                    if "td" not in position and "<b>" not in position:
                        PositionsList.append((position))
           
            for i in range(2, (len(Players) * 3), 3):
                NationList.append(str(Nationality[i]).split('title="', 1)[1].split('"/', 1)[0])
            
            for i in range(0, len(Values)):
                ValuesList.append(Values[i].text)
            #for value in ValuesList:
                #if 'm' in value:
                    #cleaned_values.append(float(value.split('m\xa0')[0].split('€')[1]) * 1000000)
                #elif 'k' in value:
                    #cleaned_values.append(float(value.split('k\xa0')[0].split('€')[1]) * 1000)
                #else:
                    #cleaned_values.append(0.0)
            
        data = zip_longest(PlayersList, ClubList, AgeList, PositionsList, NationList, ValuesList)
        df = pd.DataFrame(data, columns=['Player','Club', 'Age', 'Position', 'Nationality', "Value"])
        df.to_excel(self.caminho_arquivo, index=False)

button_generate = ctk.CTkButton(r, text="Generate",command=generate)
button_generate.pack(pady=20)

r.mainloop()