import customtkinter as ctk

from variablesGlobales import getControleurBDD as getCtrlBDD


# L'objet FramePBConnexion gere l'affichage de la Frame qui sert a retrouver ses identifiants
class FramePBConnexion(ctk.CTkFrame):
    # La classe FramePBConnexion herite de la classe ctk.CTkFrame
    def __init__(
        self, tabview, ongletPBConexion
    ):  # methode qui va etre executee a la creation de l'objet
        super().__init__(ongletPBConexion, corner_radius=0, fg_color="transparent")

        self.tabview = tabview
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=2)

        # mise ne forme fenetre de Probème de Connexion

        self.texte_oubli_entry = ctk.CTkLabel(self, text="Adresse Mail")
        self.texte_oubli_entry.grid(row=2, column=0, padx=20, pady=20)

        self.oubli_entry = ctk.CTkEntry(self)
        self.oubli_entry.grid(row=2, column=1, padx=20, pady=20)

        self.oubli_button = ctk.CTkButton(
            self,
            text="Envoyer",
            fg_color="DeepSkyBlue1",
            text_color="black",
            command=self.preparationEnvoyerMail,
        )
        self.oubli_button.grid(row=4, column=1, padx=20, pady=20)

        # Label message d'erreur
        self.texte_PBconnexion = ctk.CTkLabel(self, text="")
        self.texte_PBconnexion.grid(row=5, column=1, padx=20, pady=20)

    def preparationEnvoyerMail(self):
        mail = self.oubli_entry.get()
        getCtrlBDD().requeteEnvoyerMail(self, mail)
