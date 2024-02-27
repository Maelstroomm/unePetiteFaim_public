import customtkinter as ctk
from tkinter.filedialog import askopenfilename
from variablesGlobales import getControleurBDD as getCtrlBDD
from variablesGlobales_identifiants import obtenirIdentifiantUtilisateur, obtenirIdUtilisateur
from PIL import Image
import io
from variablesGlobales import cheminDossierData

class FrameAccueil(ctk.CTkFrame):
    def __init__(self, ihm):
        super().__init__(ihm, corner_radius=0, fg_color="transparent")
        self.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")


        
        # Message de bienvenue 
        self.bienvenu_1 = ctk.CTkLabel(self, font=("Times New Roman", 20, "bold"), text="Bonjour " +str(obtenirIdentifiantUtilisateur())+", nous sommes heureux de vous revoir !", wraplength=600,text_color="DeepSkyBlue1")
        self.bienvenu_1.place(x=240,y=30)
        self.bienvenu = ctk.CTkLabel(self, font=("Times New Roman", 20, "bold"), text="Vous avez un petit creux ?", wraplength=300,text_color="DeepSkyBlue1")
        self.bienvenu.place(x=340,y=60)

        # Statistiques
        self.nb_recettes = ctk.CTkLabel(self, font=("Times New Roman", 16, "bold"), text="Recettes répertoriées : "+str(getCtrlBDD().nb_recettes()), anchor="center")
        self.nb_recettes.place(x=100,y=130)

        self.nb_recettes_perso = ctk.CTkLabel(self, font=("Times New Roman", 16, "bold"), text="Vos recettes : "+str(getCtrlBDD().nb_recettes_perso()), anchor="center")
        self.nb_recettes_perso.place(x=400,y=130)

        self.nb_utilisateurs = ctk.CTkLabel(self, font=("Times New Roman", 16, "bold"), text="Utilisateurs : "+str(getCtrlBDD().nb_utilisateurs()), anchor="center")
        self.nb_utilisateurs.place(x=700,y=130)
        
        self.favoris = ctk.CTkLabel(self, font=("Times New Roman", 18, "bold"), text="Fonctionnement de la rubrique favoris :\nUne recette apparaîtra dans vos Favoris si elle a une note supérieure ou égale à 6. Par contre, une note de 0 la supprimera de vos sélections aléatoires.", wraplength=330)
        self.favoris.place(x=440,y=290)
                
        # image favoris
        favoris_image = ctk.CTkImage(light_image=Image.open(f"{cheminDossierData}/images/ihm/favoris.png"), size=(60, 120))
        favoris_image_label = ctk.CTkLabel(self, image=favoris_image, text="")  # display image with a CTkLabel
        favoris_image_label.place(x=800,y=280)
        
        # Contact
        self.contact_1 = ctk.CTkLabel(self, font=("Times New Roman", 16, "bold"), text="Pour toutes informations complémentaires, contactez-nous à l'adresse suivante : ")
        self.contact_1.place(x=100,y=510)
        self.contact = ctk.CTkLabel(self, font=("Times New Roman", 16, "bold"), text="unepetitefaim.mb.ap@gmail.com",text_color="DeepSkyBlue1")
        self.contact.place(x=645,y=510)

        # Image 
        
        my_image = ctk.CTkImage(light_image=Image.open(f"{cheminDossierData}/images/ihm/logo_V4.png"), size=(300, 300))
        image_label = ctk.CTkLabel(self, image=my_image, text="")  # display image with a CTkLabel
        image_label.place(x=100,y=180)# Image Favoris 

    
    """def redimensionnerImages(self, event):
        nouvelle_largeur = self.pourcentageDansLaFrame * event.width
        self.my_image.configure(size=(nouvelle_largeur,int(self.heightImageOriginale*nouvelle_largeur/self.widthImageOriginale)))
        self.image_label.configure(image=self.my_image)"""
        
        
        
        
        
        