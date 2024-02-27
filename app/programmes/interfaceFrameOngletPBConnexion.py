import customtkinter as ctk
from variablesGlobales import getControleurBDD as getCtrlBDD
import bcrypt

class FrameOngletPBConnexion(ctk.CTkFrame):
    """Cette frame permet d'afficher la frame permettant de modifier son mot de passe 
    La frame fait partie d'un TabView

    

    La classe FrameOngletPBCOnnexion herite de la classe ctk.CTkFrame
    """
    def __init__(self, tabView:ctk.CTkTabview,onglet,nomOnglet:str):
        """
        methode qui va etre executee a la creation de l'objet
        Args:
            tabView (ctk.CTkTabview): _description_
            onglet (ctk.CTkTabview.tab): objet onglet du Tabview dans laquelle est implante la frame
            nomOnglet (str): nom de l'onglet dans laquelle est implante la frame
        """
        super().__init__(onglet, corner_radius=5, fg_color="transparent")
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.nomOnglet="Modifier Mon Mot De Passe"
        self.tabView=tabView

        
        # Création de la variable de contrôle
        self.var_checkbox = ctk.BooleanVar()
        
        
        
        #mise en forme onglet pour modifier son mdp
        
        self.texte_connexion_entry = ctk.CTkLabel(self, text="Identifiant")
        self.texte_connexion_entry.grid(row=2, column=0, padx=20, pady=20)
        
        self.connexion_entry =ctk.CTkEntry(self)
        self.connexion_entry.grid(row=2, column=1, padx=20, pady=20)
        
        
        
        self.texte_mdp_entry = ctk.CTkLabel(self, text="Mot De Passe Actuel")
        self.texte_mdp_entry.grid(row=3, column=0, padx=20, pady=20)
        
        self.mdp_entry =ctk.CTkEntry(self,show="*")
        self.mdp_entry.grid(row=3, column=1, padx=20, pady=20)
        
        
        self.texte_new_mdp_entry = ctk.CTkLabel(self, text="Nouveau Mot De Passe")
        self.texte_new_mdp_entry.grid(row=4, column=0, padx=20, pady=20)
        
        self.new_mdp_entry =ctk.CTkEntry(self,show="*")
        self.new_mdp_entry.grid(row=4, column=1, padx=20, pady=20)
        
        
        
        self.connexion_button_2 = ctk.CTkButton(self,text = "Modifier",fg_color="DeepSkyBlue1",text_color="black", command= self.preparationRequeteModificationMdp )
        self.connexion_button_2.grid(row=5, column=1, padx=20, pady=20)
        
        # afficher le mdp
        self.mdp_check_button = ctk.CTkCheckBox(self,text="Voir Les Mots De Passe",variable=self.var_checkbox, command= self.afficher_mots_de_passe )
        self.mdp_check_button.grid(row=6, column=1, padx=20, pady=20)

        #Label pour afficher un message d'erreur si besoin
        self.texte_PBconnexion = ctk.CTkLabel(self,text="", wraplength=200,font=("Times New Roman", 16,"bold"),text_color="red")
        self.texte_PBconnexion.grid(row=7, column=1, padx=20, pady=20)
        
    
        
    
    def afficher_mots_de_passe(self):
        if self.var_checkbox.get():
            self.mdp_entry.configure(show="")
            self.new_mdp_entry.configure(show="")
        else:
           self.mdp_entry.configure(show="*") 
           self.new_mdp_entry.configure(show="*")
        
    def preparationRequeteModificationMdp(self):
            
        identifiant = self.connexion_entry.get()
        mdp = self.mdp_entry.get()
        
        acceptation=getCtrlBDD().requete_connexion(identifiant, mdp)
        if acceptation[0]:

            new_mdp = self.new_mdp_entry.get()
            
            if len(new_mdp)!= 0 :
            
                new_mdp_bc = bcrypt.hashpw(new_mdp.encode("utf-8"), bcrypt.gensalt())
                
                #requete de modification du mot de passe
                getCtrlBDD().requeteModifierMdp(new_mdp_bc, identifiant)

                self.texte_PBconnexion.configure(text="La modification a été prise en compte!")
                self.texte_PBconnexion.configure(text_color="DeepSkyBlue1")

                return
            else : 
                self.texte_PBconnexion.configure(text="Erreur de modification : nouveau mot de passe invalide")
                self.texte_PBconnexion.configure(text_color="red")    

        else :
            if acceptation[1] == "Erreur d'identification":
                self.texte_PBconnexion.configure(text_color="red") 
                self.texte_PBconnexion.configure(text="Erreur d'identification : mot de passe invalide")
            elif acceptation[1] == "Identifiant inconnu":
                self.texte_PBconnexion.configure(text_color="red") 
                self.texte_PBconnexion.configure(text="Identifiant inconnu. Si vous n'êtes pas inscrit, veuillez vous inscrire sur la page Nouvel Utilisateur.")
                
    

