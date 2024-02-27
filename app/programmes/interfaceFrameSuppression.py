import customtkinter as ctk
import bcrypt

# importation du fichier de l'interface principale
import interfaceGraphique as IG
from variablesGlobales import getControleurBDD as getCtrlBDD


# L'objet Framesuppression gere l'affichage de la Frame qui sert a supprimer son compte utilisateur
class Framesuppression(ctk.CTkFrame):
    # La classe Framesuppression herite de la classe ctk.CTkFrame
    def __init__(self, fenetreConexion):
        # methode qui va etre executee a la creation de l'objet
        super().__init__(fenetreConexion, corner_radius=0, fg_color="transparent")
        self.fenetreConexion = fenetreConexion

        # Création de la variable de contrôle
        self.var_checkbox = ctk.BooleanVar()

        # mise en forme fenetre de connexion

        self.texte_connexion_entry = ctk.CTkLabel(self, text="Identifiant")
        self.texte_connexion_entry.grid(row=2, column=0, padx=20, pady=20)

        self.connexion_entry = ctk.CTkEntry(self)
        self.connexion_entry.grid(row=2, column=1, padx=20, pady=20)

        self.texte_mdp_entry = ctk.CTkLabel(self, text="Mot De Passe")
        self.texte_mdp_entry.grid(row=3, column=0, padx=20, pady=20)

        self.mdp_entry = ctk.CTkEntry(self, show="*")
        self.mdp_entry.grid(row=3, column=1, padx=20, pady=20)

        self.connexion_button_2 = ctk.CTkButton(
            self,
            text="Supprimer Mon Compte",
            fg_color="DeepSkyBlue1",
            text_color="black",
            command=self.preparationRequeteSuppression,
        )
        self.connexion_button_2.grid(row=4, column=1, padx=20, pady=20)

        # afficher le mdp
        self.mdp_check_button = ctk.CTkCheckBox(
            self,
            text="Voir Le Mot De Passe",
            variable=self.var_checkbox,
            command=self.afficher_mot_de_passe,
        )
        self.mdp_check_button.grid(row=5, column=1, padx=20, pady=20)

        # Label pour afficher un message d'erreur si besoin
        self.texte_PBconnexion = ctk.CTkLabel(
            self,
            text="",
            wraplength=200,
            font=("Times New Roman", 16, "bold"),
            text_color="red",
        )
        self.texte_PBconnexion.grid(row=6, column=1, padx=20, pady=20)

    def afficher_mot_de_passe(self):
        if self.var_checkbox.get():
            self.mdp_entry.configure(show="")
        else:
            self.mdp_entry.configure(show="*")

    def preparationRequeteSuppression(self):
        identifiant = self.connexion_entry.get()
        mdp = self.mdp_entry.get()

        # requete à la bdd pour verifier l'identifiant et le mdp
        autorisation = getCtrlBDD().requete_connexion(identifiant, mdp)

        if autorisation[0] == True:
            getCtrlBDD().suppression_compte(autorisation[1], identifiant)
            self.texte_PBconnexion.configure(text="Votre compte a été supprimé!")
            return
        else:
            if autorisation[1] == "Erreur d'identification":
                self.texte_PBconnexion.configure(
                    text="Erreur d'identification : mot de passe invalide"
                )
            elif autorisation[1] == "Identifiant inconnu":
                self.texte_PBconnexion.configure(
                    text="Identifiant inconnu. Si vous n'êtes pas inscrit, veuillez vous inscrire sur la page Nouvel Utilisateur."
                )
