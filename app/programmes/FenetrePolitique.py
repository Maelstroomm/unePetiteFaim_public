import customtkinter as ctk
from tkinter import PhotoImage
from variablesGlobales import cheminDossierData

class FrameTexte(ctk.CTkScrollableFrame):
    def __init__(self, FenetrePolitique):
        super().__init__(FenetrePolitique)

        # Chemin vers le fichier texte a afficher
        fichier_texte = f"{cheminDossierData}/Politique.txt"

        # Lecture du fichier texte
        with open(fichier_texte, 'r', encoding='utf-8') as file:
            contenu = file.read()

        # Affichage du contenu du fichier
        self.label = ctk.CTkLabel(self, text=contenu, wraplength=500, justify ='left',font=("Times New Roman", 16))
        self.label.grid(row=0, column=0, padx=20, pady=20)

class FenetrePolitique(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        #icon_path = f"{cheminDossierData}/images/ihm/icone_V3.ico"   
        #self.iconbitmap(icon_path)
        #icone = PhotoImage(file=f"{cheminDossierData}/images/ihm/icone_V3.gif")
        #self.iconphoto(True, icone)


        self.title('Politique de Confidentialité')
        self.geometry('600x400')
        self.resizable(height=True, width=True)

        self.FrameTexte = FrameTexte(self)
        self.FrameTexte.grid(row=0, column=0, sticky="nsew")

        # Configurer la répartition des cellules de la grille pour occuper toute la fenêtre
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)



#programme principal :
if __name__ == "__main__":
    app_3 = FenetrePolitique()
    app_3.mainloop()
