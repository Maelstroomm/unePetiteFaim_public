import customtkinter as ctk
from random import randint

# importation du fichier qui contient la classe FrameRecherche
import interfaceFrameRecherche as frRecherhce

# importation du fichier qui contient la classe FrameOngletRecette
import interfaceFrameOngletRecette as frRecette

# importation du fichier qui contient la classe BoutonApercuRecette
import interfaceApercuRecette as frApercu


class TabViewRechercheResultat(ctk.CTkTabview):
    """Frame à onglet qui va servir à faire une recherche (1er onglet) et afficher les differentes recettes (2eme onglet et +)"""

    def __init__(self, fentrePrincipale: ctk.CTk):
        """
        Args:
            fentrePrincipale (ctk.CTk): Fenetre dans laquelle va etre implante la TabView
        """
        super().__init__(fentrePrincipale)
        self.ihm = fentrePrincipale
        # Liste qui va contenir tous les objets d'apercu des recettes
        self.listeApercu = []
        # Liste qui va contenir tous les objets onglet recettes
        self.listeOnglets = []

        # Onglet de recherche
        self.add("Recherche")
        recherche = self.tab("Recherche")
        recherche.grid_columnconfigure(0, weight=1)
        recherche.grid_rowconfigure(0, weight=1)
        recherche.grid_rowconfigure(1, weight=5)
        self.frameRecherche = frRecherhce.FrameRecherche(self, recherche)
        self.frameRecherche.grid(row=0, column=0, sticky="nsew", rowspan=2)

        # frame dediee à l'affichage et la selection du classement de la recherche
        frameClassement = ctk.CTkFrame(recherche, fg_color="transparent")
        frameClassement.grid(row=0, column=1, sticky="ew")

        labelClassement = ctk.CTkLabel(
            frameClassement, text="Classer par : ", anchor="center"
        )
        labelClassement.grid(row=0, column=0, sticky="ew", columnspan=2)

        self.classement_var = ctk.StringVar()
        classementRadioBoutonNom = ctk.CTkRadioButton(
            frameClassement,
            text="Nom",
            variable=self.classement_var,
            value="Nom",
            command=self.frameRecherche.recupererDonnees,
        )
        classementRadioBoutonNom.grid(row=1, column=0)
        classementRadioBoutonNom.select()
        classementRadioBoutonNote = ctk.CTkRadioButton(
            frameClassement,
            text="Note",
            variable=self.classement_var,
            value="Note",
            command=self.frameRecherche.recupererDonnees,
        )
        classementRadioBoutonNote.grid(row=1, column=1)

        ## frame pour afficher les possibilites de recette : cette frame va accueillir les frames Apercu Recettes
        self.framePossibilite = ctk.CTkScrollableFrame(
            recherche, fg_color="transparent", width=160
        )
        self.framePossibilite.grid(row=1, column=1, sticky="nsew")

        # Label texte pour afficher qu'y n'y a aucun resultat pour la recherche
        self.labelPasDeResultat = ctk.CTkLabel(
            self.framePossibilite,
            text="Oups, aucune recette ne correspond à la recherche",
            wraplength=120,
            anchor="center",
        )

    def afficherApercu(self, listeRecette: list):
        """Cette fonction est appelee par le bouton rechercher de la frame Rechercher.
        Permet d'afficher un apecu de la recette (nom et image) dans la framePossibilite

        Args:
            listeRecette (list): liste de tuple de toutes les recettes correspondant à la recherche
                                    avec le format : [(nom1, image1, idPlat1), (nom2, image2, idPlat2), ...]
        """
        # Supprimer tous les appercus deja presents:
        for i in range(len(self.listeApercu)):
            self.listeApercu[i].pack_forget()
            self.listeApercu[i].destroy()

        if len(listeRecette) == 0:  # si aucun resultat ne correspond a la recherche
            self.labelPasDeResultat.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        else:
            self.labelPasDeResultat.grid_forget()  # enlever le message pour dire qu'il n'y a pas de resultat
            if self.frameRecherche.aleatoire == 0:
                for i in range(len(listeRecette)):
                    self.listeApercu.append(
                        frApercu.FrameApercuRecette(
                            self,
                            self.framePossibilite,
                            i,
                            listeRecette[i][2],
                            listeRecette[i][0],
                            listeRecette[i][1],
                        )
                    )
            elif (
                len(listeRecette) > 0
            ):  # si la recherche aleatoire est cochee : on affiche qu'un apercu parmis toutes les recettes renvoyee par la bdd
                indice = randint(0, len(listeRecette) - 1)

                self.listeApercu.append(
                    frApercu.FrameApercuRecette(
                        self,
                        self.framePossibilite,
                        indice,
                        listeRecette[indice][2],
                        listeRecette[indice][0],
                        listeRecette[indice][1],
                    )
                )

    def creerOngletRecette(self, idPlat: int, nomOnglet: str):
        """Cette fonction est appelee lors d'un clic sur un apercu de recette
            - Lors du premier clic : creation d'un nouvel onglet et d'une FrameOngletRecette pour afficher la recette, sans l'afficher au premier plan
            - Lors des clics suivants : l'onglet actif devient celui de la recette

        Args:
            idPlat (int)
            nomOnglet (str): _description_
        """
        if nomOnglet not in self.listeOnglets:
            # Onglets des Recettes
            self.add(nomOnglet)
            onglet = self.tab(nomOnglet)
            onglet.grid_columnconfigure(0, weight=1)
            onglet.grid_rowconfigure(0, weight=1)
            self.frameRecette = frRecette.FrameOngletRecette(
                self, onglet, nomOnglet, idPlat
            )
            self.frameRecette.grid(row=0, column=0, sticky="nsew")
            self.listeOnglets.append(nomOnglet)
            self.set(
                nomOnglet
            )  # pour que l'onglet que l'on vient de creer soit celui en cours d'affichage

        else:
            self.set(
                nomOnglet
            )  # pour que l'onglet que l'on vient de creer soit celui en cours d'affichage

    def fermerOnglet(self, nomOnglet: str):
        """Cette fonction est appellee par le bouton Fermer de l'onglet recette
            Permet de supprimer l'onglet correspondant
        Args:
            nomOnglet (str): nom de l'onglet a fermer
        """
        self.delete(nomOnglet)
        self.listeOnglets.remove(nomOnglet)
