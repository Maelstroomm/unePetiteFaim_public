import customtkinter as ctk
from random import randint

#importation du fichier qui contient la classe FramePBConnexion
import interfaceFramePBConnexion as frPBConnexion
#importation du fichier qui contient la classe FrameOngletPBConnexion
import interfaceFrameOngletPBConnexion as frOngletPBConnexion


class TabViewPBConnexion(ctk.CTkTabview):
    """Frame à onglet qui va servir à demander ses identifiants (1er onglet) et modifier son mdp (2eme onglet et +)
    """
    def __init__(self,fentrePrincipale:ctk.CTk):
        """
        Args:
            fentrePrincipale (ctk.CTk): Fenetre dans laquelle va etre implante la TabView
        """
        super().__init__(fentrePrincipale)
        

        # Liste qui va contenir tous les objets onglet recettes
        nomOnglet="Modifier mon mot de passe"
        
        #Onglet demnde d'indentifiants
        self.add("Mes Identifiants ?")
        recherche=self.tab("Mes Identifiants ?")
        recherche.grid_columnconfigure(0, weight=1)
        recherche.grid_rowconfigure(0, weight=1)
        recherche.grid_rowconfigure(1, weight=5)
        self.frameOubli=frPBConnexion.FramePBConnexion(self,recherche)
        self.frameOubli.grid(row=0,column=0,sticky="nsew", rowspan=2)
   
        self.add(nomOnglet)
        onglet=self.tab(nomOnglet)
        onglet.grid_columnconfigure(0, weight=1)
        onglet.grid_rowconfigure(0, weight=1)
        self.frameOubli=frOngletPBConnexion.FrameOngletPBConnexion(self,onglet,nomOnglet)
        self.frameOubli.grid(row=0,column=0,sticky="nsew")
