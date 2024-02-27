import customtkinter as ctk
from variablesGlobales import getControleurBDD as getCtrlBDD


class FrameRecherche(ctk.CTkScrollableFrame):
    # La classe FrameRecherche herite de la classe ctk.CTkScrollableFrame
    def __init__(
        self, tabview, onglet
    ):  # methode qui va etre executee a la creation de l'objet
        super().__init__(
            onglet, corner_radius=5, fg_color="transparent"
        )  # ,label_text="Rechercher une recette")
        self.tabview = tabview
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=2)

        # Champs de Recherche
        self.entryRecherche = ctk.CTkEntry(
            self, placeholder_text="Exemple : Galette des Rois", corner_radius=20
        )
        self.entryRecherche.grid(
            row=2, column=2, columnspan=2, padx=20, pady=15, sticky="nsew"
        )

        # Type de Repas
        listeTypeRepas = [
            "Non Renseigné",
            "Apéritif",
            "Entrée",
            "Plat",
            "Dessert ou Goûter",
        ]

        self.labelTypeRepas = ctk.CTkLabel(
            self, text="Partie du repas : ", anchor="center"
        )
        self.labelTypeRepas.grid(row=4, column=1, padx=20, pady=15, sticky="nsew")

        self.optionmenuTypeRepas = ctk.CTkOptionMenu(self, values=listeTypeRepas)
        self.optionmenuTypeRepas.set(listeTypeRepas[0])
        self.optionmenuTypeRepas.grid(row=4, column=2, padx=20, pady=15, sticky="nsew")

        # Type de Plat
        listeTypePlats = [
            "Non Renseigné",
            "Viande",
            "Poisson",
            "Soupe",
            "Glace",
            "Gâteau",
            "Laitage",
            "Viennoiserie",
            "Pizza",
            "Tarte",
            "Pâte",
            "Salade",
            "Accompagnement",
            "Végétarien",
        ]

        self.labelTypePlat = ctk.CTkLabel(self, text="Type de plat : ", anchor="center")
        self.labelTypePlat.grid(row=5, column=1, padx=20, pady=15, sticky="nsew")

        self.optionmenuTypePlat = ctk.CTkOptionMenu(self, values=listeTypePlats)
        self.optionmenuTypePlat.set(listeTypePlats[0])
        self.optionmenuTypePlat.grid(row=5, column=2, padx=20, pady=15, sticky="nsew")

        # Saisons
        listeSaisons = ["Toutes", "Eté", "Hiver", "Printemps", "Automne"]

        self.labelSaison = ctk.CTkLabel(self, text="Saison : ", anchor="center")
        self.labelSaison.grid(row=6, column=1, padx=20, pady=15, sticky="nsew")

        self.optionmenuSaison = ctk.CTkOptionMenu(self, values=listeSaisons)
        self.optionmenuSaison.grid(row=6, column=2, padx=20, pady=15, sticky="nsew")

        # creation d'une frame dediee a la selection du temps de preparation
        frameTempsP = ctk.CTkFrame(self, fg_color="transparent")
        frameTempsP.grid(row=7, column=2, columnspan=2, sticky="ew")
        frameTempsP.grid_columnconfigure(1, weight=3)
        frameTempsP.grid_columnconfigure(2, weight=1)
        frameTempsP.grid_columnconfigure(3, weight=3)
        frameTempsP.grid_columnconfigure(4, weight=1)

        # Temps préparation
        listeHeures = [str(i) for i in range(0, 25)]
        listeMinutes = [str(i) for i in range(0, 60, 5)]

        self.switchvarPrepa = ctk.StringVar(value="off")
        self.switchPrepa = ctk.CTkSwitch(
            self,
            command=self.switch_eventP,
            text="Temps de préparation inferieur à : ",
            variable=self.switchvarPrepa,
            onvalue="on",
            offvalue="off",
        )
        self.switchPrepa.grid(row=7, column=1, padx=20, pady=15, sticky="nsew")

        self.optionmenuTpsPrepaHeure = ctk.CTkOptionMenu(
            frameTempsP, values=listeHeures
        )
        self.optionmenuTpsPrepaHeure.grid(
            row=0, column=1, padx=(20, 0), pady=15, sticky="ew"
        )
        self.optionmenuTpsPrepaHeure.configure(state="disabled")

        self.labelH = ctk.CTkLabel(frameTempsP, text="h", anchor="center")
        self.labelH.grid(row=0, column=2, padx=0, pady=15, sticky="ew")

        self.optionmenuTpsPrepaMin = ctk.CTkOptionMenu(frameTempsP, values=listeMinutes)
        self.optionmenuTpsPrepaMin.grid(row=0, column=3, padx=0, pady=15, sticky="ew")
        self.optionmenuTpsPrepaMin.configure(state="disabled")

        self.labelMin = ctk.CTkLabel(frameTempsP, text="min", anchor="center")
        self.labelMin.grid(row=0, column=4, padx=(5, 20), pady=15, sticky="ew")

        # creation d'une frame dediee a la selection du temps de cuisson
        frameTempsC = ctk.CTkFrame(self, fg_color="transparent")
        frameTempsC.grid(row=8, column=2, columnspan=2, sticky="ew")
        frameTempsC.grid_columnconfigure(1, weight=3)
        frameTempsC.grid_columnconfigure(2, weight=1)
        frameTempsC.grid_columnconfigure(3, weight=3)
        frameTempsC.grid_columnconfigure(4, weight=1)

        # Temps cuisson
        self.switchvarCuisson = ctk.StringVar(value="off")
        self.switchCuisson = ctk.CTkSwitch(
            self,
            text="Temps de cuisson inferieur à :",
            command=self.switch_eventC,
            variable=self.switchvarCuisson,
            onvalue="on",
            offvalue="off",
        )
        self.switchCuisson.grid(row=8, column=1, padx=20, pady=15, sticky="nsew")

        self.optionmenuTpsCuissonHeure = ctk.CTkOptionMenu(
            frameTempsC, values=listeHeures
        )
        self.optionmenuTpsCuissonHeure.grid(
            row=0, column=1, padx=(20, 0), pady=15, sticky="ew"
        )
        self.optionmenuTpsCuissonHeure.configure(state="disabled")

        self.labelH2 = ctk.CTkLabel(frameTempsC, text="h", anchor="center")
        self.labelH2.grid(row=0, column=2, padx=0, pady=15, sticky="ew")

        self.optionmenuTpsCuissonMin = ctk.CTkOptionMenu(
            frameTempsC, values=listeMinutes
        )
        self.optionmenuTpsCuissonMin.grid(row=0, column=3, padx=0, pady=15, sticky="ew")
        self.optionmenuTpsCuissonMin.configure(state="disabled")

        self.labelMin2 = ctk.CTkLabel(frameTempsC, text="min", anchor="center")
        self.labelMin2.grid(row=0, column=4, padx=(5, 20), pady=15, sticky="ew")

        # Ustensiles
        self.labelUstensiles = ctk.CTkLabel(
            self, text="Sans les ustensiles : ", anchor="center"
        )
        self.labelUstensiles.grid(row=13, column=1, padx=20, pady=15, sticky="nsew")

        self.frameUstensiles = ctk.CTkFrame(self, fg_color="transparent")
        self.frameUstensiles.grid(row=13, column=2, columnspan=3, padx=20, pady=15)

        self.listeUstensiles = [
            "Four",
            "Cocotte minute",
            "Mixeur",
            "Batteur éléctrique",
            "Balance",
            "Verre doseur",
            "Multicuiseur",
            "Autres appareils spécifiques",
        ]
        self.listeCheckboxUstensiles = []
        for i in range(len(self.listeUstensiles)):
            tempo = ctk.CTkCheckBox(self.frameUstensiles, text=self.listeUstensiles[i])
            tempo.grid(row=i // 2, column=i % 2, padx=20, pady=5, sticky="ew")
            self.listeCheckboxUstensiles.append(tempo)

        # Auteur
        listeAuteurs = ["Tous"] + getCtrlBDD().requeteRecupererTousUtilisateurs()
        self.labelAuteur = ctk.CTkLabel(self, text="Auteur ", anchor="center")
        self.labelAuteur.grid(row=15, column=1, padx=20, pady=15, sticky="nsew")

        self.optionmenuAuteur = ctk.CTkOptionMenu(self, values=listeAuteurs)
        self.optionmenuAuteur.set(listeAuteurs[0])
        self.optionmenuAuteur.grid(row=15, column=2, padx=20, pady=15, sticky="nsew")
        # Recerhcer dans
        listeNote = ["Tous", "Favoris", "Recettes sans note"]
        self.labelNote = ctk.CTkLabel(self, text="Rechercher dans ", anchor="center")
        self.labelNote.grid(row=16, column=1, padx=20, pady=15, sticky="nsew")

        self.optionmenuNote = ctk.CTkOptionMenu(self, values=listeNote)
        self.optionmenuNote.set(listeNote[0])
        self.optionmenuNote.grid(row=16, column=2, padx=20, pady=15, sticky="nsew")

        # Aleatoire:
        self.checkbokAlea = ctk.CTkCheckBox(self, text="Recherche Aléatoire")
        self.checkbokAlea.grid(row=17, column=2, padx=20, pady=15, sticky="nsew")

        # Bouton Rechercher haut
        self.boutonRechercher = ctk.CTkButton(
            self, text="Rechercher", command=self.recupererDonnees, corner_radius=20
        )
        self.boutonRechercher.grid(row=2, column=1, padx=20, pady=15, sticky="nsew")

        # Bouton Rechercher bas
        self.boutonRechercher = ctk.CTkButton(
            self, text="Rechercher", command=self.recupererDonnees, corner_radius=20
        )
        self.boutonRechercher.grid(
            row=18, column=1, padx=20, pady=15, sticky="nsew", columnspan=2
        )

    def slider_event(self, valeur):
        self.varNombreParts.set(value=round(valeur))

    def switch_eventC(self):
        """
        Permet de desactiver la selection du temps de cuisson si il n'y a pas de cuisson
        """
        # print("switch toggled, current value:", self.switchvarCuisson.get())
        position = self.switchvarCuisson.get()
        if position == "off":
            self.optionmenuTpsCuissonHeure.configure(state="disabled")
            self.optionmenuTpsCuissonMin.configure(state="disabled")
        else:
            self.optionmenuTpsCuissonHeure.configure(state="normal")
            self.optionmenuTpsCuissonMin.configure(state="normal")

    def switch_eventP(self):
        """
        Permet de desactiver la selection du temps de preparation
        """
        # print("switch toggled, current value:", self.switchvarPrepa.get())
        position = self.switchvarPrepa.get()
        if position == "off":
            self.optionmenuTpsPrepaHeure.configure(state="disabled")
            self.optionmenuTpsPrepaMin.configure(state="disabled")
        else:
            self.optionmenuTpsPrepaHeure.configure(state="normal")
            self.optionmenuTpsPrepaMin.configure(state="normal")

    # a transformer en liste
    def getUstensile(self) -> str:
        """
        Renvoie une liste de tous les ustensiles selectionnes
        """
        ustensiles = []
        for i in range(len(self.listeCheckboxUstensiles)):
            if self.listeCheckboxUstensiles[i].get() == 1:
                ustensiles.append(self.listeUstensiles[i])
        return ustensiles

    def recupererDonnees(self):
        """
        Recupere tous les champs rentre dans l'onglet Recherche
        """
        self.recherche = self.entryRecherche.get()
        self.typeRepas = self.optionmenuTypeRepas.get()
        self.typePlat = self.optionmenuTypePlat.get()
        self.typeSaison = self.optionmenuSaison.get()
        self.preparation = self.switchvarPrepa.get()
        self.tpsPrepaH = self.optionmenuTpsPrepaHeure.get()  # tps min
        self.tpsPrepaMin = self.optionmenuTpsPrepaMin.get()  # tps min
        self.cuisson = self.switchvarCuisson.get()
        self.tpsCuissonH = self.optionmenuTpsCuissonHeure.get()  # tps min
        self.tpsCuissonMin = self.optionmenuTpsCuissonMin.get()  # tps min
        self.ustensiles = self.getUstensile()  # ustensiles a ne pas utiliser
        self.auteur = self.optionmenuAuteur.get()
        self.aleatoire = self.checkbokAlea.get()
        self.favoris = self.optionmenuNote.get()
        self.classement = self.tabview.classement_var.get()

        reponse = getCtrlBDD().requeteRechercher(self)

        self.tabview.afficherApercu(reponse)
