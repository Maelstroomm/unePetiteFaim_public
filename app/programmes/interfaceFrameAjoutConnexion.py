import customtkinter as ctk

# importation du fichier qui contient la classe Fenetre Politique
import FenetrePolitique as fePolitique

from chiffrerEmail import securiserMail, desecuriserMail
from variablesGlobales import getControleurBDD as getCtrlBDD


# L'objet FrameAjoutConnexion gere l'affichage de la Frame qui sert a ajouter un utilisateur
class FrameAjoutConnexion(ctk.CTkFrame):
    # La classe FrameAjoutConnexion herite de la classe ctk.CTkFrame
    def __init__(
        self, fenetreConexion
    ):  # methode qui va etre executee a la creation de l'objet
        super().__init__(fenetreConexion, corner_radius=0, fg_color="transparent")

        # Création de la variable de contrôle de l'affichage du mdp
        self.var_checkbox = ctk.BooleanVar()

        # Création de la variable de contrôle de l'acceptation des conditions générales
        self.var_Politique_checkbox = ctk.BooleanVar()

        # création du lien
        self.texte_Politique = ctk.CTkTextbox(self)

        #
        self.Politique_button = ctk.CTkButton(
            self,
            text="Politique",
            fg_color="DeepSkyBlue1",
            text_color="black",
            command=self.Politique,
        )
        self.Politique_button.configure(
            font=("Times New Roman", 10, "bold"), width=2, height=2
        )
        self.Politique_button.grid(row=5, column=2, padx=0, pady=20)

        # mise ne forme fenetre d'ajout

        self.texte_ajout_entry = ctk.CTkLabel(self, text="Identifiant")
        self.texte_ajout_entry.grid(row=2, column=0, padx=20, pady=20)

        self.ajout_entry = ctk.CTkEntry(self)
        self.ajout_entry.grid(row=2, column=1, padx=20, pady=20)

        self.texte_mdp_ajout_entry = ctk.CTkLabel(self, text="Mot De Passe")
        self.texte_mdp_ajout_entry.grid(row=3, column=0, padx=20, pady=20)

        self.mdp_ajout_entry = ctk.CTkEntry(self, show="*")
        self.mdp_ajout_entry.grid(row=3, column=1, padx=20, pady=20)

        self.texte_ajout_mail_entry = ctk.CTkLabel(self, text="Adresse Mail")
        self.texte_ajout_mail_entry.grid(row=4, column=0, padx=20, pady=20)

        self.ajout_mail_entry = ctk.CTkEntry(self)
        self.ajout_mail_entry.grid(row=4, column=1, padx=20, pady=20)

        self.ajout_button = ctk.CTkButton(
            self,
            text="S'enregistrer",
            fg_color="DeepSkyBlue1",
            text_color="black",
            command=self.preparationRequeteAjoutConnexion,
        )
        self.ajout_button.grid(row=7, column=1, padx=20, pady=20)

        # afficher le mdp
        self.mdp_ajout_button = ctk.CTkCheckBox(
            self,
            text="Voir Le Mot De Passe",
            variable=self.var_checkbox,
            command=self.afficher_mot_de_passe,
        )
        self.mdp_ajout_button.grid(row=6, column=1, padx=20, pady=20)

        # accepter la politique de confidentialité

        self.Politique_button_check = ctk.CTkCheckBox(
            self,
            text="J'accepte la politique de confidentialité ",
            variable=self.var_Politique_checkbox,
        )
        self.Politique_button_check.configure(font=("Times New Roman", 10, "bold"))
        self.Politique_button_check.grid(row=5, column=1, padx=0, pady=5)

        # affichage erreur de saisi
        self.texte_PB_AjConnexion = ctk.CTkLabel(self, text="")
        self.texte_PB_AjConnexion.configure(
            font=("Times New Roman", 16, "bold"), text_color="red"
        )
        self.texte_PB_AjConnexion.grid(row=8, column=1, padx=20, pady=20)

    def afficher_mot_de_passe(self):
        if self.var_checkbox.get():
            self.mdp_ajout_entry.configure(show="")
        else:
            self.mdp_ajout_entry.configure(show="*")

    def Politique(self):
        # visualiser la politique

        app_3 = fePolitique.FenetrePolitique()  # creation de l'objet
        app_3.mainloop()

    def preparationRequeteAjoutConnexion(self):
        mdp = self.mdp_ajout_entry.get()
        identifiant = self.ajout_entry.get()
        mail = self.ajout_mail_entry.get()

        # Verification de l'unicite du mail et de l'identifiant
        unicite_identifiant = True
        unicite_mail = True

        result = getCtrlBDD().requeteUniciteUtilisateur()
        if result:
            for ligne in result:
                if ligne[0] == identifiant:
                    unicite_identifiant = False
                    break

                elif desecuriserMail(ligne[1]) == mail:
                    unicite_mail = False
                    break

        # print(unicite_identifiant,unicite_mail)

        if unicite_identifiant == False:
            self.texte_PB_AjConnexion.configure(
                text="Erreur : Identifiant déjà existant",
                font=("Times New Roman", 16, "bold"),
                text_color="red",
            )

        # vérification du remplissage du champs mdp
        elif len(mdp) == 0:
            self.texte_PB_AjConnexion.configure(
                text="Erreur : Mot de passe trop court ",
                font=("Times New Roman", 16, "bold"),
                text_color="red",
            )

        elif unicite_mail == False:
            self.texte_PB_AjConnexion.configure(
                text="Erreur : Mail déjà utilisé",
                font=("Times New Roman", 16, "bold"),
                text_color="red",
            )

        # vérification politique acceptée
        elif self.var_Politique_checkbox.get() == False:
            self.texte_PB_AjConnexion.configure(
                text="Erreur : Vous devez accepter la politique ",
                font=("Times New Roman", 16, "bold"),
                text_color="red",
            )

        # vérification du mail
        elif "@" in mail:
            getCtrlBDD().requeteAjoutUtilisateur(mdp, identifiant, securiserMail(mail))

            self.texte_PB_AjConnexion.configure(
                text="Votre profil a été créé avec succès! ",
                font=("Times New Roman", 16, "bold"),
                text_color="DeepSkyBlue1",
            )

        else:
            self.texte_PB_AjConnexion.configure(
                text="Erreur : Mail incorrect",
                font=("Times New Roman", 16, "bold"),
                text_color="red",
            )
