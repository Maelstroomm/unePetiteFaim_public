import customtkinter as ctk


class FenetreVersion(ctk.CTk):
    def __init__(self, version_actuelle:int, nouvelle_version:int):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")


        self.title('Une Petite Faim : Mise à jour requise')
        self.geometry('600x400')
        self.resizable(height=True, width=True)

        self.labelTexte = ctk.CTkLabel(self, text="Cher utilisateur,\n\
Nous tenons à vous informer qu'une mise à jour importante de l'application est disponible. Pour continuer à profiter pleinement de nos services et fonctionnalités, veuillez télécharger la dernière version dès maintenant.\n\
Si vous avez des questions ou avez besoin d'assistance, notre équipe de support client est à votre disposition pour vous aider à l'adresse suivante : unepetitefaim.mb.ap@gmail.com.\n\
Nous vous remercions de votre compréhension et de votre coopération.",wraplength=500, justify ='left',font=("Times New Roman", 16))

        self.labelTexte.grid(row=0, column=0, padx=20, pady=(30,10),sticky="nsew")

        self.labelInformations = ctk.CTkLabel(self, text=f"Informations complémentaires : \n \
Votre numéro de version : {version_actuelle}\n \
Nouvelle version requise: {nouvelle_version}",wraplength=500, justify ='center',font=("Times New Roman", 16))

        self.labelInformations.grid(row=1, column=0, padx=20, pady=(10,30),sticky="nsew")

        # Configurer la répartition des cellules de la grille pour occuper toute la fenêtre
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)



#programme principal :
if __name__ == "__main__":
    app_3 = FenetreVersion(1.0,1.2)
    app_3.mainloop()
