import customtkinter as ctk
from tkinter import PhotoImage

#####Import des fichier utiles
# importation du fichier qui contient la classe FrameAjout
import interfaceFrameAjout as frAjout

# importation du fichier qui contient la classe FrameAccueil
import interfaceFrameAccueil as frAccueil
import interfaceTabViewRechercheResultat as frtvRecherhceResultat

# importation de la fonction modifierIdentifiantEtIdUtilisateur qui se trouve dans le fichier variablesGlobales
from variablesGlobales_identifiants import modifierIdentifiantEtIdUtilisateur

from variablesGlobales import getControleurBDD as getCtrlBDD, cheminDossierData


class App(ctk.CTk):
    # La classe APP herite de la classe ctk.CTk
    # methode __init__ qui va etre executee a la creation de l'objet
    def __init__(self, identifiant, idUtilisateur):
        super().__init__()
        # appeler la fonction qui permet de definir de maniere global l'idUtilisateur
        modifierIdentifiantEtIdUtilisateur(idUtilisateur, identifiant)

        getCtrlBDD().fenetre = self
        # création de la fenetre de l'IHM
        self.title("Une Petite Faim")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.geometry("1200x600")
        self.resizable(height=True, width=True)

        # icon_path = f"{cheminDossierData}/images/ihm/icone_V3.ico"
        # self.iconbitmap(icon_path)
        icone = PhotoImage(file=f"{cheminDossierData}/images/ihm/icone_V3.gif")
        self.iconphoto(True, icone)

        # definir les lignes et les colones de la fenetre
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # définir les differentes frames qu'on va utiliser
        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        # create second frame
        self.home_frame = frAccueil.FrameAccueil(self)
        # create third frame
        # self.recherche_frame = frRecherhce.FrameRecherche(self) #on va chercher l'objet FrameRecherche dans le fichier interfaceFrameAjout.py
        self.recherche_frame = frtvRecherhceResultat.TabViewRechercheResultat(self)
        # create 4th frame
        self.ajout_frame = frAjout.FrameAjout(self)

        #####frame de navigation sur la gauche
        # mettre en forme la navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_titre = ctk.CTkLabel(
            self.navigation_frame,
            text="Une Petite Faim",
            compound="left",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.navigation_frame_titre.grid(row=0, column=0, padx=20, pady=20)

        # bouton pour acceder a la frame d'accueil
        self.home_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Accueil",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.home_button_event,
        )
        self.home_button.grid(row=1, column=0, sticky="ew")

        # bouton pour acceder a la frame recherche
        self.frame_recherche_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Rechercher",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.frame_recherche_button_event,
        )
        self.frame_recherche_button.grid(row=2, column=0, sticky="ew")

        # bouton pour acceder a la frame d'Ajout
        self.frame_ajout_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Ajouter",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.frame_ajout_button_event,
        )
        self.frame_ajout_button.grid(row=3, column=0, sticky="ew")

        # bouton pour acceder a la frame de Modification
        self.frame_modif_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Modifier",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.frame_modif_button_event,
        )

        # pour afficher des messages d'erreur
        self.labelInformation = ctk.CTkLabel(
            self.navigation_frame, text="", text_color="red"
        )
        self.labelInformation.grid(row=5, column=0)

        # bouton pour changer l'aparance dark/light
        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.navigation_frame,
            values=["Dark", "Light", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # pour changer le zoom
        self.zoom_label = ctk.CTkLabel(
            self.navigation_frame, text="Zoom : ", anchor="w"
        )
        self.zoom_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.zoom_optionemenu = ctk.CTkOptionMenu(
            self.navigation_frame,
            values=[
                "30%",
                "40%",
                "50%",
                "60%",
                "70%",
                "80%",
                "90%",
                "100%",
                "110%",
                "120%",
                "130%",
            ],
            command=self.change_zoom_event,
        )
        self.zoom_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        self.zoom_optionemenu.set("100%")

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        """
        methode qui sert à afficher la frame correspondante au bouton clique
        """
        # set button color for selected button
        self.home_button.configure(
            fg_color=("gray75", "gray25") if name == "home" else "transparent"
        )
        self.frame_recherche_button.configure(
            fg_color=("gray75", "gray25") if name == "recherche" else "transparent"
        )
        self.frame_ajout_button.configure(
            fg_color=("gray75", "gray25") if name == "ajout" else "transparent"
        )
        self.frame_modif_button.configure(
            fg_color=("gray75", "gray25") if name == "modif" else "transparent"
        )

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "recherche":
            self.recherche_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.recherche_frame.grid_forget()
        if name == "ajout":
            self.ajout_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.ajout_frame.grid_forget()
        if name == "modif":
            self.modif_frame.grid(row=0, column=1, sticky="nsew")
        else:
            try:
                self.modif_frame.grid_forget()
            except:
                pass

    def creer_frame_modifier(self, idPlat):
        """Creer la frame Modifier et l'affiche

        Args:
            idPlat (_type_): idPlat de la rrecette a modifier
        """
        # create 5th frame
        self.modif_frame = frAjout.FrameModifier(self, idPlat)
        self.frame_modif_button.grid(row=4, column=0, sticky="ew")
        self.frame_modif_button_event()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_recherche_button_event(self):
        self.select_frame_by_name("recherche")

    def frame_ajout_button_event(self):
        self.select_frame_by_name("ajout")

    def frame_modif_button_event(self):
        self.select_frame_by_name("modif")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_zoom_event(self, new_zoom: str):
        new_zoom_float = int(new_zoom.replace("%", "")) / 100
        ctk.set_widget_scaling(new_zoom_float)

    def afficherInformation(self, info: str):
        self.labelInformation.configure(text=info)

    def effacerInformation(self):
        self.labelInformation.configure(text="")

    def fermerFrameModification(self, nomOngletAFermer: str):
        self.home_button_event()
        self.modif_frame.grid_forget()
        self.frame_modif_button.grid_forget()
        self.recherche_frame.fermerOnglet(nomOngletAFermer)

    def annulerFrameModification(self):
        self.frame_recherche_button_event()
        self.modif_frame.grid_forget()
        self.frame_modif_button.grid_forget()


# programme principal :
if __name__ == "__main__":
    app = App("mael123", 9)  # creation de l'objet avec le profil de test
    app.mainloop()
