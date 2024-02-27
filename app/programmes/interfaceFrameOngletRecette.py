import customtkinter as ctk
from PIL import Image
from functools import partial
from variablesGlobales import getControleurBDD as getCtrlBDD
from datetime import timedelta, datetime
import io
from variablesGlobales import cheminDossierData
from variablesGlobales_identifiants import obtenirIdentifiantUtilisateur


class FrameOngletRecette(ctk.CTkScrollableFrame):
    """Cette frame permet d'afficher une recette et toutes les infos la concernant
    La frame fait partie d'un TabView



    La classe FrameOngletRecette herite de la classe ctk.CTkScrollableFrame
    """

    def __init__(self, tabView: ctk.CTkTabview, onglet, nomOnglet: str, idPlat: int):
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

        self.nomOnglet = nomOnglet
        self.idRecette = 0
        self.tabView = tabView

        # requete a la bdd
        listeInfos = getCtrlBDD().requeteAfficherRecetteParID(idPlat)
        # et reccuperation des informations:
        self.idPlat = listeInfos[0]
        nomRecette = listeInfos[1]
        recette = listeInfos[2]
        saison = listeInfos[5]
        difficulte = listeInfos[6]

        tpsPrepa = listeInfos[7]
        tpsCuisson = listeInfos[8]
        if tpsCuisson == None:  # gestion du tps de cuisson facultatif
            tpsCuisson = "-"
            tpsCuissonCalcul = self.convertirDuree("00:00")
        else:
            tpsCuissonCalcul = self.convertirDuree(str(tpsCuisson))
            tpsCuisson = self.affichageDuree(str(tpsCuisson))
        # calcul du tps total
        tpsTotal = self.convertirDuree(str(tpsPrepa)) + tpsCuissonCalcul

        nbreParts = listeInfos[9]
        ustensiles = listeInfos[11]
        if ustensiles == None:
            ustensiles = "-"
        imageBinaire = listeInfos[13]
        auteur = listeInfos[14]
        source = listeInfos[15]
        dateCreation = listeInfos[16]

        # Bouton Fermer
        boutonFermer = ctk.CTkButton(
            self,
            text="Fermer",
            command=partial(self.tabView.fermerOnglet, self.nomOnglet),
        )
        boutonFermer.grid(row=0, column=2, padx=20, pady=(15, 2), sticky="e")

        # Bouton Modifier: Uniquement si l'utilisateur est l'auteur de la recette
        if auteur == obtenirIdentifiantUtilisateur():
            boutonModifier = ctk.CTkButton(
                self,
                text="Modifier",
                command=partial(self.tabView.ihm.creer_frame_modifier, self.idPlat),
            )
            boutonModifier.grid(row=1, column=2, padx=20, pady=(2, 15), sticky="e")

        # creation d'une frame dediee au choix de la note
        frameNote = ctk.CTkFrame(self, corner_radius=20, fg_color="transparent")
        frameNote.grid(row=0, column=1, sticky="w", padx=20, pady=20)
        frameNote.grid_columnconfigure(1, weight=2)
        frameNote.grid_columnconfigure(2, weight=2)
        frameNote.grid_columnconfigure(3, weight=1)

        # Note
        listeNote = [" ", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

        labelNote = ctk.CTkLabel(frameNote, text="Note : ", anchor="center")
        labelNote.grid(row=0, column=0, padx=0, pady=0, sticky="w")

        self.optionmenuNote = ctk.CTkOptionMenu(frameNote, values=listeNote, width=75)
        self.optionmenuNote.grid(row=0, column=1, padx=5, pady=0, sticky="w")

        self.boutonNote = ctk.CTkButton(
            frameNote, text="OK", command=self.getNote, width=20
        )
        self.boutonNote.grid(row=0, column=2, padx=(0, 10), pady=0, sticky="w")

        self.afficherFavoris()

        # Nom de la recette
        labelNomRecette = ctk.CTkLabel(self, text=nomRecette, anchor="center")
        labelNomRecette.grid(
            row=2, column=1, padx=20, pady=15, sticky="nsew", columnspan=2
        )

        # creation d'une frame dediee a l'affichage des differents temps
        frameTemps = ctk.CTkFrame(
            self, corner_radius=20, fg_color=("#b0b5b6", "#333333")
        )
        frameTemps.grid(row=5, column=1, columnspan=2, sticky="ew", padx=20, pady=20)
        frameTemps.grid_columnconfigure(0, weight=1)
        frameTemps.grid_columnconfigure(1, weight=1)

        labelTempsTotal = ctk.CTkLabel(
            frameTemps,
            text="Temps total :   " + self.affichageDuree(str(tpsTotal)),
            anchor="center",
            bg_color="transparent",
        )
        labelTempsTotal.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        labelTempspPrepa = ctk.CTkLabel(
            frameTemps,
            text="Préparation :   " + self.affichageDuree(str(tpsPrepa)),
            anchor="center",
            bg_color="transparent",
        )
        labelTempspPrepa.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        labelTempsCuisson = ctk.CTkLabel(
            frameTemps,
            text="Cuisson :   " + tpsCuisson,
            anchor="center",
            bg_color="transparent",
        )
        labelTempsCuisson.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Image
        self.pourcentageDansLaFrame = 0.2
        largeurOnglet = self.cget("width")
        largeurImage = self.pourcentageDansLaFrame * largeurOnglet

        if imageBinaire == None:
            img = Image.open(f"{cheminDossierData}/images/ihm/IHMimage.png")
            self.widthImageOriginale, self.heightImageOriginale = img.size
            self.my_image = ctk.CTkImage(
                light_image=img, size=(largeurImage, largeurImage)
            )
        else:
            img = Image.open(io.BytesIO(imageBinaire))
            self.widthImageOriginale, self.heightImageOriginale = img.size
            self.my_image = ctk.CTkImage(
                light_image=img,
                size=(
                    largeurImage,
                    int(
                        self.heightImageOriginale
                        * largeurImage
                        / self.widthImageOriginale
                    ),
                ),
            )

        # Lier la fonction de redimensionnement à l'événement de changement de taille de la frame
        frameTemps.bind("<Configure>", self.redimensionner_image)

        self.image_label = ctk.CTkLabel(
            self, image=self.my_image, text=""
        )  # display image with a CTkLabel
        self.image_label.grid(
            row=4, column=1, columnspan=2, padx=20, pady=15, sticky="nsew"
        )

        # creation d'une frame dediee a l'affichage des differents informations
        frameInfos = ctk.CTkFrame(
            self, corner_radius=20, fg_color=("#b0b5b6", "#333333")
        )
        frameInfos.grid(row=7, column=1, columnspan=2, sticky="ew", padx=20, pady=5)
        frameInfos.grid_columnconfigure(1, weight=1)

        # Difficulte
        labelRecette = ctk.CTkLabel(
            frameInfos, text="Difficulté :   " + difficulte, anchor="center"
        )
        labelRecette.grid(row=12, column=1, padx=20, pady=5, sticky="w")

        # Nombre de parts
        labelRecette = ctk.CTkLabel(
            frameInfos, text="Nombre de part(s) :   " + str(nbreParts), anchor="center"
        )
        labelRecette.grid(row=13, column=1, padx=20, pady=5, sticky="w")

        # Saison
        labelRecette = ctk.CTkLabel(
            frameInfos, text="Saison :   " + saison, anchor="center"
        )
        labelRecette.grid(row=14, column=1, padx=20, pady=5, sticky="w")

        # Ustensiles
        labelUstensiles = ctk.CTkLabel(
            frameInfos, text="Ustensiles nécessaire :   " + ustensiles, anchor="center"
        )
        labelUstensiles.grid(row=15, column=1, padx=20, pady=5, sticky="w")

        # Recette
        labelRecette = ctk.CTkLabel(self, text="Recette : ", anchor="center")
        labelRecette.grid(
            row=16, column=1, padx=20, pady=(15, 5), sticky="nsew", columnspan=2
        )

        textboxRecette = ctk.CTkTextbox(self, corner_radius=5, height=500)
        textboxRecette.grid(
            row=17, column=1, padx=20, pady=(5, 15), sticky="nsew", columnspan=2
        )
        textboxRecette.insert(ctk.END, recette)

        # Source
        labelSource = ctk.CTkLabel(self, text="Source :   " + source, anchor="center")
        labelSource.grid(
            row=19, column=1, padx=20, pady=(10, 5), sticky="w", columnspan=2
        )

        # Auteur et date de creation
        labelAuteur = ctk.CTkLabel(
            self,
            text="Recette ajoutée par "
            + auteur
            + " le "
            + self.affichageDate(dateCreation),
            anchor="center",
        )
        labelAuteur.grid(row=20, column=1, padx=20, pady=5, sticky="w", columnspan=2)

    def afficherFavoris(self):
        note = getCtrlBDD().requeteObtenirNoteFavoris(self.idPlat)
        if note != None:
            self.optionmenuNote.set(str(note))

    def getNote(self):
        """
        Recupere la note selectionnee par l'utiliateur
        """
        note = self.optionmenuNote.get()
        print("Note de la recette : ", note)
        if note != " ":
            getCtrlBDD().requeteAjoutFavoris(self.idPlat, int(note))
            self.boutonNote.configure(fg_color="forestgreen")

    def convertirDuree(self, heureMinute: str) -> timedelta:
        """Convertit une str de la forme HH:MM dans le format timedelta pour pouvoir additioner des durees

        Args:
            heureMinute (str): chaine de carectere dans la forme TIME de SQLITE : HH:MM

        Returns:
            timedelta: duree du type timedelta
        """
        listeHeureMinute = heureMinute.split(":")
        return timedelta(
            hours=int(listeHeureMinute[0]), minutes=int(listeHeureMinute[1])
        )

    def affichageDuree(self, heureMinute: str) -> str:
        """Permet l'Affichage propre d'une duree:
                - si il n'y a que des minutes : 'MM min'
                - si il y a des heures et minutes :
                        - si l'heure contient qu'un chiffre : 'H h MM'
                        - si l'heure contient 2 chiffres : 'HH h MM'

        Args:
            heureMinute (str): chaine de carectere dans la forme TIME de SQLITE : 'HH:MM'
                                ou '-' dans le cas ou le tps de cuisson n'est pas renseigne

        Returns:
            str: duree pret a etre affichee
        """
        if heureMinute != "-":
            heureMinute = heureMinute.split(":")
            heures = heureMinute[0]
            if heures[0] == "0" and len(heures) == 2:  # cas 0H:MM
                heures = heures[1]
            minutes = heureMinute[1]
            if heures == "00" or heures == "0":  # cas 00:MM ou 0:MM
                return f"{minutes} min"
            else:
                return f"{heures} h {minutes}"
        else:
            return heureMinute

    def affichageDate(self, date: datetime) -> str:
        return date.strftime("%d/%m/%Y")

    def redimensionner_image(self, event):
        """Fonction qui est appelee des que la fenetre est redimensionnee
        Permet de redimensionner l'image en consequence
        Args:
            event (_type_): _description_
        """
        if self.tabView.get() == self.nomOnglet:
            nouvelle_largeur = self.pourcentageDansLaFrame * event.width
            self.my_image.configure(
                size=(
                    nouvelle_largeur,
                    int(
                        self.heightImageOriginale
                        * nouvelle_largeur
                        / self.widthImageOriginale
                    ),
                )
            )
            self.image_label.configure(image=self.my_image)
