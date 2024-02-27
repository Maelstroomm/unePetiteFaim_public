import os
import customtkinter as ctk
from functools import partial
from tkinter.filedialog import askopenfilename
from variablesGlobales import getControleurBDD as getCtrlBDD


class FrameAjoutEtModifier(ctk.CTkScrollableFrame):
    """
    Cette frame est la composante graphique qui permet d'ajouter une recette dans la bdd
    La classe FrameAjout herite de la classe ctk.CTkScrollableFrame
    """

    def __init__(self, ihm: ctk.CTk, titreFrame: str):
        """
        methode qui va etre executee a la creation de l'objet
        Args:
            ihm (ctk.CTk): application dans laquelle va etre integrer cette frame
        """

        super().__init__(
            ihm,
            corner_radius=5,
            fg_color="transparent",
            label_text=titreFrame,
        )
        self.ihm = ihm
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Placement des widgets

        # Nom de la recette
        self.labelNomRecette = ctk.CTkLabel(
            self, text="Nom de la recette : ", anchor="center"
        )
        self.labelNomRecette.grid(row=2, column=1, padx=20, pady=15, sticky="nsew")

        self.entryNomRecette = ctk.CTkEntry(
            self, placeholder_text="Entrez le nom de la recette"
        )
        self.entryNomRecette.grid(row=2, column=2, padx=20, pady=15, sticky="nsew")

        # Type de Repas
        listeTypeRepas = ["Apéritif", "Entrée", "Plat", "Dessert ou Goûter"]

        self.labelTypeRepas = ctk.CTkLabel(
            self, text="Partie du repas : ", anchor="center"
        )
        self.labelTypeRepas.grid(row=3, column=1, padx=20, pady=15, sticky="nsew")

        self.optionmenuTypeRepas = ctk.CTkOptionMenu(self, values=listeTypeRepas)
        self.optionmenuTypeRepas.set(listeTypeRepas[2])
        self.optionmenuTypeRepas.grid(row=3, column=2, padx=20, pady=15, sticky="nsew")

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
        self.labelTypePlat.grid(row=4, column=1, padx=20, pady=15, sticky="nsew")

        self.optionmenuTypePlat = ctk.CTkOptionMenu(self, values=listeTypePlats)
        self.optionmenuTypePlat.set(listeTypePlats[0])
        self.optionmenuTypePlat.grid(row=4, column=2, padx=20, pady=15, sticky="nsew")

        # Saisons
        listeSaisons = ["Toutes", "Eté", "Hiver", "Printemps", "Automne"]

        self.labelSaison = ctk.CTkLabel(self, text="Saison : ", anchor="center")
        self.labelSaison.grid(row=5, column=1, padx=20, pady=15, sticky="nsew")

        self.optionmenuSaison = ctk.CTkOptionMenu(self, values=listeSaisons)
        self.optionmenuSaison.grid(row=5, column=2, padx=20, pady=15, sticky="nsew")

        # Difficulte
        listeDifficulte = ["*", "**", "***"]

        self.labelDifficulte = ctk.CTkLabel(self, text="Difficulté : ", anchor="center")
        self.labelDifficulte.grid(row=6, column=1, padx=20, pady=15, sticky="nsew")

        self.segbuttonDifficulte = ctk.CTkSegmentedButton(self, values=listeDifficulte)
        self.segbuttonDifficulte.set(listeDifficulte[1])
        self.segbuttonDifficulte.grid(row=6, column=2, padx=20, pady=15, sticky="nsew")

        # creation d'une frame dediee a la selection du temps de preparation
        frameTempsP = ctk.CTkFrame(self, fg_color="transparent")
        frameTempsP.grid(row=7, column=2, sticky="ew")
        frameTempsP.grid_columnconfigure(0, weight=3)
        frameTempsP.grid_columnconfigure(1, weight=1)
        frameTempsP.grid_columnconfigure(2, weight=3)
        frameTempsP.grid_columnconfigure(3, weight=1)

        # Temps préparation
        listeHeures = [str(i) for i in range(0, 25)]
        listeMinutes = [str(i) for i in range(0, 60, 5)]

        self.labelTpsPreparation = ctk.CTkLabel(
            self, text="Temps de préparation : ", anchor="center"
        )
        self.labelTpsPreparation.grid(row=7, column=1, padx=20, pady=15, sticky="nsew")

        self.optionmenuTpsPrepaHeure = ctk.CTkOptionMenu(
            frameTempsP, values=listeHeures
        )
        self.optionmenuTpsPrepaHeure.grid(
            row=0, column=0, padx=(20, 0), pady=15, sticky="ew"
        )

        self.labelH = ctk.CTkLabel(frameTempsP, text="h", anchor="center")
        self.labelH.grid(row=0, column=1, padx=0, pady=15, sticky="ew")

        self.optionmenuTpsPrepaMin = ctk.CTkOptionMenu(frameTempsP, values=listeMinutes)
        self.optionmenuTpsPrepaMin.grid(row=0, column=2, padx=0, pady=15, sticky="ew")

        self.labelMin = ctk.CTkLabel(frameTempsP, text="min", anchor="center")
        self.labelMin.grid(row=0, column=3, padx=(0, 20), pady=15, sticky="ew")

        # creation d'une frame dediee a la selection du temps de cuisson
        frameTempsC = ctk.CTkFrame(self, fg_color="transparent")
        frameTempsC.grid(row=8, column=2, sticky="ew")
        frameTempsC.grid_columnconfigure(0, weight=2)
        frameTempsC.grid_columnconfigure(1, weight=3)
        frameTempsC.grid_columnconfigure(2, weight=1)
        frameTempsC.grid_columnconfigure(3, weight=3)
        frameTempsC.grid_columnconfigure(4, weight=1)

        # Temps cuisson
        self.labelTpsCuisson = ctk.CTkLabel(
            self, text="Temps de cuisson : ", anchor="center"
        )
        self.labelTpsCuisson.grid(row=8, column=1, padx=20, pady=15, sticky="nsew")

        self.switch_var = ctk.StringVar(value="off")
        self.switch = ctk.CTkSwitch(
            frameTempsC,
            text="Cuisson",
            command=self.switch_event,
            variable=self.switch_var,
            onvalue="on",
            offvalue="off",
        )
        self.switch.grid(row=0, column=0, padx=20, pady=15, sticky="nsew")

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
        self.labelMin2.grid(row=0, column=4, padx=(0, 20), pady=15, sticky="ew")

        # creation d'une frame dediee a la selection du nombre de parts
        frameNbrePart = ctk.CTkFrame(self, fg_color="transparent")
        frameNbrePart.grid(row=9, column=2, sticky="ew")
        frameNbrePart.grid_columnconfigure(0, weight=1)
        frameNbrePart.grid_columnconfigure(1, weight=5)

        # Nombre de parts
        self.labelNbreParts = ctk.CTkLabel(
            self, text="Nombre de parts : ", anchor="center"
        )
        self.labelNbreParts.grid(row=9, column=1, padx=20, pady=15, sticky="nsew")

        self.slider = ctk.CTkSlider(
            frameNbrePart, from_=0, to=20, number_of_steps=20, command=self.slider_event
        )
        self.slider.set(2)
        self.slider.grid(row=0, column=1, padx=20, pady=15, sticky="nsew")

        self.varNombreParts = ctk.StringVar(value="2")

        self.labelAfficheNbreParts = ctk.CTkLabel(
            frameNbrePart, textvariable=self.varNombreParts, anchor="center"
        )
        self.labelAfficheNbreParts.grid(
            row=0, column=0, padx=20, pady=15, sticky="nsew"
        )

        framePhoto = ctk.CTkFrame(self, fg_color="transparent")
        framePhoto.grid(row=10, column=2, sticky="ew")
        framePhoto.grid_columnconfigure(0, weight=2)
        framePhoto.grid_columnconfigure(1, weight=1)

        # Photo
        self.labelPhoto = ctk.CTkLabel(self, text="Photo : ", anchor="center")
        self.labelPhoto.grid(row=10, column=1, padx=20, pady=15, sticky="nsew")

        self.boutonPhoto = ctk.CTkButton(
            framePhoto, text="Ouvrir une image", command=self.ouvrirImage
        )
        self.boutonPhoto.grid(row=0, column=0, padx=20, pady=15, sticky="nsew")

        self.labelNomPhoto = ctk.CTkLabel(
            framePhoto, text="              ", anchor="center", wraplength=300
        )
        self.labelNomPhoto.grid(row=0, column=1, padx=20, pady=15, sticky="nsew")

        self.cheminImage = None

        # Recette
        self.labelRecette = ctk.CTkLabel(self, text="Recette : ", anchor="center")
        self.labelRecette.grid(row=11, column=1, padx=20, pady=15, sticky="nsew")

        self.textboxRecette = ctk.CTkTextbox(self, corner_radius=0)
        self.textboxRecette.grid(row=11, column=2, padx=20, pady=15, sticky="nsew")

        # Source
        self.labelSource = ctk.CTkLabel(self, text="Source : ", anchor="center")
        self.labelSource.grid(row=12, column=1, padx=20, pady=15, sticky="nsew")

        self.entrySource = ctk.CTkEntry(
            self, placeholder_text="Entrez la source de la recette"
        )
        self.entrySource.grid(row=12, column=2, padx=20, pady=15, sticky="nsew")

        # Ustensiles
        self.labelUstensiles = ctk.CTkLabel(
            self, text="Ustensiles nécessaires : ", anchor="center"
        )
        self.labelUstensiles.grid(row=13, column=1, padx=20, pady=15, sticky="nsew")

        self.frameUstensiles = ctk.CTkFrame(self, fg_color="transparent")
        self.frameUstensiles.grid(row=13, column=2, padx=20, pady=15)

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
            tempo = ctk.CTkCheckBox(
                self.frameUstensiles,
                text=self.listeUstensiles[i],
            )
            tempo.grid(row=i // 2, column=i % 2, padx=20, pady=5, sticky="ew")
            self.listeCheckboxUstensiles.append(tempo)

        # Mots cles
        # self.labelMotsCles = ctk.CTkLabel(self, text="Mots clés : ", anchor="center")
        # self.labelMotsCles.grid(row=14, column=1, padx=20, pady=15, sticky="nsew")

        # Bouton valider
        self.boutonValider = ctk.CTkButton(
            self,
            fg_color="DeepSkyBlue1",
            text_color="black",
            text="Valider",
            command=self.recupererDonnees,
        )
        self.boutonValider.grid(
            row=16, column=1, padx=20, pady=15, sticky="nsew", columnspan=2
        )
        # self.boutonValider.configure(fg_color="DeepSkyBlue1")

        # afficher la frame
        self.grid(row=1, column=2, padx=(20, 50), pady=(20, 50), sticky="nsew")

    def slider_event(self, valeur: int):
        """Fonction qui recupere la valeur du slider nombre de parts

        Args:
            valeur (int): nombre de parts
        """
        self.varNombreParts.set(value=round(valeur))

    def switch_event(self):
        """
        Est appele lors d'un clique sur la switch tps de cuisson.
        Permet de desactiver la selection du temps de cuisson si il n'y a pas de cuisson
        """

        position = self.switch_var.get()  # recuperer la position
        if position == "off":
            self.optionmenuTpsCuissonHeure.configure(state="disabled")
            self.optionmenuTpsCuissonMin.configure(state="disabled")
        else:
            self.optionmenuTpsCuissonHeure.configure(state="normal")
            self.optionmenuTpsCuissonMin.configure(state="normal")

    def ouvrirImage(self):
        """
        Permet de charger une image au format jpg, jpeg, png
        Recupere uniquement le chemin vers l'image
        Verifie que l'image n'est pas trop grosse
        """
        # boite de dialogue qui recupere le chemin d'acces
        self.cheminImage = askopenfilename(
            title="Charger une image",
            filetypes=[("Image", "*.jpg"), ("Image", "*.jpeg"), ("Image", "*.png")],
        )

        # Vérifier la taille du fichier sélectionné
        taille_max = 41943040  # 40Mo

        if self.cheminImage:
            taille_fichier = os.path.getsize(self.cheminImage)
            if taille_fichier > taille_max:
                print("La taille du fichier dépasse la limite autorisee.")
                self.cheminImage = None
                self.labelNomPhoto.configure(
                    text="Merci de selectionner une image \n pesant moins de 40 Mo"
                )
            else:
                print("Fichier sélectionné :", self.cheminImage)
                nomPhoto = self.cheminImage.split("/")[-1]
                self.labelNomPhoto.configure(text=nomPhoto)
        else:
            self.cheminImage = None
            self.labelNomPhoto.configure(text="              ")

    def getUstensile(self) -> str:
        """
        Renvoie un chaine de caractere de tous les ustensiles selectionnes separes par un ;
        """
        strUstensiles = ""
        for i in range(len(self.listeCheckboxUstensiles)):
            if self.listeCheckboxUstensiles[i].get() == 1:
                strUstensiles += self.listeUstensiles[i] + ";"
        strUstensiles = strUstensiles[:-1]  # on enleve le dernier ;
        return strUstensiles

    def recupererDonnees(self, modification: bool = False):
        """
        Recupere tous les champs rentre dans la frame
        """
        nomRecette = self.entryNomRecette.get()
        recette = self.textboxRecette.get(index1="1.0", index2=ctk.END)  # a voir
        typeRepas = self.optionmenuTypeRepas.get()
        typePlat = self.optionmenuTypePlat.get()
        typeSaison = self.optionmenuSaison.get()
        difficulte = self.segbuttonDifficulte.get()
        tpsPrepaH = self.optionmenuTpsPrepaHeure.get()
        tpsPrepaMin = self.optionmenuTpsPrepaMin.get()
        cuisson = self.switch_var.get()
        tpsCuissonH = self.optionmenuTpsCuissonHeure.get()
        tpsCuissonMin = self.optionmenuTpsCuissonMin.get()
        nombreParts = self.varNombreParts.get()
        source = self.entrySource.get()
        ustensiles = self.getUstensile()

        if modification:
            resultatRequete = getCtrlBDD().requeteModifierRecette(
                self.idPlat_initial,
                self.nomRecette_initial,
                self.recette_initial,
                self.typeRepas_initial,
                self.typePlat_initial,
                self.saison_initial,
                self.difficulte_initial,
                self.tpsPrepa_initial,
                self.tpsCuisson_initial,
                self.nbreParts_initial,
                self.ustensiles_initial,
                self.source_initial,
                nomRecette,
                recette,
                typeRepas,
                typePlat,
                typeSaison,
                difficulte,
                tpsPrepaH,
                tpsPrepaMin,
                tpsCuissonH,
                cuisson,
                tpsCuissonMin,
                nombreParts,
                ustensiles,
                source,
                self.cheminImage,
            )
        else:
            resultatRequete = getCtrlBDD().requeteAjoutRecette(
                nomRecette,
                recette,
                typeRepas,
                typePlat,
                typeSaison,
                difficulte,
                tpsPrepaH,
                tpsPrepaMin,
                tpsCuissonH,
                cuisson,
                tpsCuissonMin,
                nombreParts,
                ustensiles,
                source,
                self.cheminImage,
            )

        if resultatRequete == "Faux_nom":
            """
            self.entryNomRecette.configure(placeholder_text="Nom déjà utilisé")
            On ne peut plus modifier le texte mais que le placeholder
            """

            self.labelNomRecette.configure(text_color="red")
            self.boutonValider.configure(fg_color="red")
            self.labelRecette.configure(text_color="white")

        elif resultatRequete == "Tout_Faux":
            self.labelRecette.configure(text_color="red")
            self.labelNomRecette.configure(text_color="red")
            self.boutonValider.configure(fg_color="red")

        elif resultatRequete == "Faux_recette":
            self.labelRecette.configure(text_color="red")
            self.boutonValider.configure(fg_color="red")
            self.labelNomRecette.configure(text_color="white")

        else:
            self.labelNomRecette.configure(text_color="white")
            self.labelRecette.configure(text_color="white")
            self.boutonValider.configure(fg_color="forestgreen")
            if modification:
                self.fermerFrameModif()


class FrameAjout(FrameAjoutEtModifier):
    def __init__(self, ihm: ctk.CTk):
        super().__init__(ihm, "Ajoutez votre recette")


class FrameModifier(FrameAjoutEtModifier):
    def __init__(self, ihm: ctk.CTk, idPlat):
        super().__init__(ihm, "Modifiez votre recette")
        self.boutonValider.configure(
            text="Enregistrer les modifications",
            command=partial(self.recupererDonnees, True),
        )
        # Bouton annuler
        self.boutonAnnuler = ctk.CTkButton(
            self,
            fg_color="DeepSkyBlue1",
            text_color="black",
            text="Annuler",
            command=self.annulerFrameModif,
        )

        self.boutonAnnuler.grid(row=16, column=1, padx=20, pady=15, sticky="nsew")
        self.boutonValider.grid(row=16, column=2, padx=20, pady=15, sticky="nsew")

        self.recupererInfoRecetteBdd(idPlat)
        self.afficherValeursInitiales()

    def recupererInfoRecetteBdd(self, idPlat):
        """Recuperer et stocke dans des variable l'ensemble des info (presents dans la bdd)de la recette dont l'identifiant est idPlat"""
        # requete a la bdd
        listeInfosRecette = getCtrlBDD().requeteAfficherRecetteParID(idPlat)

        # et reccuperation des informations:
        self.idPlat_initial = listeInfosRecette[0]
        self.nomRecette_initial = listeInfosRecette[1]
        self.recette_initial = listeInfosRecette[2]
        self.typeRepas_initial = listeInfosRecette[3]
        self.typePlat_initial = listeInfosRecette[4]
        self.saison_initial = listeInfosRecette[5]
        self.difficulte_initial = listeInfosRecette[6]

        self.tpsPrepa_initial = listeInfosRecette[7]
        self.tpsCuisson_initial = listeInfosRecette[8]

        self.nbreParts_initial = listeInfosRecette[9]
        self.ustensiles_initial = listeInfosRecette[11]

        self.imageBinaire_initial = listeInfosRecette[13]
        self.source_initial = listeInfosRecette[15]

    def afficherValeursInitiales(self):
        """Affiche dans la frame les valeurs initiales (avant modification, cad les infos stockees dans la bdd)"""
        self.entryNomRecette.insert(0, self.nomRecette_initial)
        self.optionmenuTypeRepas.set(self.typeRepas_initial)
        if self.typePlat_initial is not None:
            self.optionmenuTypePlat.set(self.typePlat_initial)
        self.optionmenuSaison.set(self.saison_initial)
        self.segbuttonDifficulte.set(self.difficulte_initial)
        # Tps prépa
        self.optionmenuTpsPrepaHeure.set(str(self.tpsPrepa_initial.hour))
        self.optionmenuTpsPrepaMin.set(str(self.tpsPrepa_initial.minute))
        # Tps cuisson
        if self.tpsCuisson_initial is not None:
            self.switch.toggle()
            self.optionmenuTpsCuissonHeure.set(str(self.tpsCuisson_initial.hour))
            self.optionmenuTpsCuissonMin.set(str(self.tpsCuisson_initial.minute))

        self.slider.set(int(self.nbreParts_initial))
        # image
        if self.imageBinaire_initial is not None:
            self.labelNomPhoto.configure(
                text="Une image est déja sauvegardée,\ncliquez pour la remplacer"
            )
        else:
            self.labelNomPhoto.configure(text="Image par défaut")
        self.textboxRecette.insert("0.0", self.recette_initial)
        self.entrySource.insert(0, self.source_initial)
        # ustensiles
        if self.ustensiles_initial != "":
            listeUstensiles_initial = self.ustensiles_initial.split(";")
            for ustensile in listeUstensiles_initial:
                index_in_liste = self.listeUstensiles.index(ustensile)
                self.listeCheckboxUstensiles[index_in_liste].select()

    def fermerFrameModif(self):
        self.ihm.fermerFrameModification(self.nomRecette_initial)

    def annulerFrameModif(self):
        self.ihm.annulerFrameModification()
