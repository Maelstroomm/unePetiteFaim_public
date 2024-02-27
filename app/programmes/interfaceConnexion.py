import customtkinter as ctk
from tkinter import PhotoImage

#####Import des fichier utiles
# importation du fichier qui contient la classe FrameIdentification
import interfaceIdentification as frIdentification

# importation du fichier qui contient la classe FramePBConnexion
import interfaceTabViewPBConnexion as frTabViewPBConnexion

# importation du fichier qui contient la classe FrameAjoutConnexion
import interfaceFrameAjoutConnexion as frAjoutConnexion

# importation du fichier qui contient la classe Framesuppression
import interfaceFrameSuppression as frSuppression
from variablesGlobales import getControleurBDD as getCtrlBDD, creerControleurBDD
from FenetreVersion import FenetreVersion
from variablesGlobales import cheminDossierData


class FenetreConnexion(ctk.CTk):
    # La classe APP herite de la classe customtkinter.CTk
    def __init__(self):
        super().__init__()

        # Definir le controleurBDD
        creerControleurBDD()
        getCtrlBDD().fenetre = self

        bonneVersion, num_version_bdd = getCtrlBDD().requeteVerificationVersion()

        if bonneVersion:
            # Si c'est la bonne version, on lance l'appli
            self.initialiserFenetreConnexion()
        else:
            # si la version n'est pas la bonne, on ouvre la fenetre invitant à faire la maj
            self.destroy()  # Détruit complètement la fenêtre actuelle
            self.quit()  # Arrête la boucle principale de la fenêtre actuelle
            app_fentetreVersion = FenetreVersion(
                getCtrlBDD().version, num_version_bdd
            )  # creation de l'objet
            app_fentetreVersion.mainloop()

    def initialiserFenetreConnexion(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # création de la fenetre de l'IHM de connexion
        self.geometry("700x500")
        self.title("Une Petite Faim")
        self.resizable(height=True, width=True)

        # icon_path = f"{cheminDossierData}/images/ihm/icone_V3.ico"
        # self.iconbitmap(icon_path)
        icone = PhotoImage(file=f"{cheminDossierData}/images/ihm/icone_V3.gif")
        self.iconphoto(True, icone)

        # definir les lignes et les colones de la fenetre
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # définir les diferentes frames qu'on va utiliser

        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)

        # create second frame
        self.connexion_frame = frIdentification.FrameIdentification(
            self
        )  # on va chercher l'objet FrameAjout dans le fichier interfaceIdentification.py

        # create third frame
        self.sign_up_frame = frAjoutConnexion.FrameAjoutConnexion(
            self
        )  # on va chercher l'objet FrameAjout dans le fichier interfaceFrameAjoutConnexion.py

        # create 4th frame
        self.oubli_frame = frTabViewPBConnexion.TabViewPBConnexion(
            self
        )  # on va chercher l'objet FrameAjout dans le fichier interfaceFramePBConnexion.py

        # create 5th frame
        self.suppression_frame = frSuppression.Framesuppression(
            self
        )  # on va chercher l'objet Framesuppression dans le fichier interfaceFrameSuppression.py

        #####frame de navigation sur la gauche
        # mettre en forme la navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)

        self.navigation_frame_titre = ctk.CTkLabel(
            self.navigation_frame,
            text="Page De Connexion",
            compound="left",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.navigation_frame_titre.grid(row=0, column=0, padx=20, pady=20)

        # bouton pour acceder a la frame d'acceuil
        self.connexion_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="M'identifier",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.connexion_button_event,
        )
        self.connexion_button.grid(row=1, column=0, sticky="ew")

        # bouton pour acceder a la frame recherche
        self.frame_sign_up_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Nouvel Utilisateur",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.frame_sign_up_button_event,
        )
        self.frame_sign_up_button.grid(row=2, column=0, sticky="ew")

        # bouton pour acceder a la frame PB Connexion
        self.frame_oubli_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Problème De Connexion",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.frame_oubli_button_event,
        )
        self.frame_oubli_button.grid(row=3, column=0, sticky="ew")

        # bouton pour acceder a la frame Suppression de compte
        self.frame_suppression_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Supprimer Mon Compte",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.frame_suppression_button_event,
        )
        self.frame_suppression_button.grid(row=4, column=0, sticky="ew")

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

        # select default frame
        self.select_frame_by_name("connexion")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.connexion_button.configure(
            fg_color=("gray75", "gray25") if name == "connexion" else "transparent"
        )
        self.frame_sign_up_button.configure(
            fg_color=("gray75", "gray25") if name == "sign" else "transparent"
        )
        self.frame_oubli_button.configure(
            fg_color=("gray75", "gray25") if name == "oubli" else "transparent"
        )
        self.frame_suppression_button.configure(
            fg_color=("gray75", "gray25") if name == "supprimer" else "transparent"
        )

        # show selected frame
        if name == "connexion":
            self.connexion_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.connexion_frame.grid_forget()
        if name == "sign":
            self.sign_up_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.sign_up_frame.grid_forget()

        if name == "oubli":
            self.oubli_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.oubli_frame.grid_forget()

        if name == "supprimer":
            self.suppression_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.suppression_frame.grid_forget()

    def connexion_button_event(self):
        self.select_frame_by_name("connexion")

    def frame_sign_up_button_event(self):
        self.select_frame_by_name("sign")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    def frame_oubli_button_event(self):
        self.select_frame_by_name("oubli")

    def frame_suppression_button_event(self):
        self.select_frame_by_name("supprimer")

    def afficherInformation(self, info: str):
        self.labelInformation.configure(text=info)

    def effacerInformation(self):
        self.labelInformation.configure(text="")


def printInfosLancement():
    print("Lancement de l'application Une Petite Faim")
    print("L'application devrait se lancer dans quelques secondes.")
    print(
        "Dans cette version, l'application pourrait ne pas demarrer du premier coup. Si cela se produit, suivez ces etapes :"
    )
    print("     1. Attendez que l'application se ferme d'elle même")
    print("     2. Relancez l'application une deuxieme fois.")
    print("     3. Attendez de nouveau que l'application se ferme d'elle même")
    print("     4. Relancez l'application une troisieme fois.")
    print(
        "Dans tous les cas, au bout du troisieme lancement, l'application devrait demarrer correctement.\n"
    )
    print("Merci de votre comprehension.\n")
    print(
        "Pour toute question, n'hesitez pas a nous contacter a l'adresse : unepetitefaim.mb.ap@gmail.com"
    )
    print("#################################")
    print("Informations de fonctionnement : ")


# programme principal :
if __name__ == "__main__":
    printInfosLancement()
    app = FenetreConnexion()  # creation de l'objet
    app.mainloop()
