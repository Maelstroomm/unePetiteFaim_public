import bcrypt
from datetime import datetime, date

from variablesGlobales_identifiants import (
    obtenirIdentifiantUtilisateur,
    obtenirIdUtilisateur,
)
from objetRequete import Requete

from mdp import (
    bdd_database,
    bdd_password,
    bdd_server,
    bdd_username,
    mail_adresse_expediteur,
    mail_mot_de_passe,
)

# importation pour generer un mdp aleatoire
import random
import string


# importation module pour l'envoie des mails
import ssl
import smtplib
from email.message import EmailMessage
from chiffrerEmail import desecuriserMail


class ControleurBDD:
    """Cet objet est chargee de gerer les interactions avec la base de donnee"""

    def __init__(self):
        """initialisation du controlleur de la base de donnee"""
        self.fenetre = None
        self.version = 1.2  # version actuelle

        # Informations de connection
        driver = "{ODBC Driver 18 for SQL Server}"
        self.connect_string = f"DRIVER={driver};SERVER={bdd_server};DATABASE={bdd_database};UID={bdd_username};PWD={bdd_password}"

    def miseEnFormeTIME(self, heure: str, minute: str) -> datetime.time:
        """Convertit les heures minutes en format SQL HH:MM

        Args:
            heure (str): heure saisie dans l'interface graphique
            minute (str): minute saisie dans l'interface graphique

        Returns:
            datetime: date au format datetime accepte par SQLITE sous le format HH:MM:SS (SS=00)
        """
        # Conversion en format DATETIME python
        time_sql = datetime.strptime(heure + ":" + minute, "%H:%M").time()
        return time_sql

    def requeteVerificationVersion(self) -> tuple:
        """
        Renvoie True si le numero de version de la base de donnee est le meme que celui stocker dans ce programme
        Renvoie False sinon
        Renvoie aussi le numéro de version stockee dans la bdd
        """
        objReq = Requete(
            "SELECT numeroVersion FROM [dbo].[VERSION] where etat ='actif' ORDER BY numeroVersion DESC;"
        )

        liste_version_bdd = self.executerRequete(objReq, True, False)

        for ligne in liste_version_bdd:
            print(ligne)
            version_bdd = ligne[0]
            if version_bdd == self.version:
                print(
                    f"Version de la bdd : {version_bdd}\nVersion de l'appli en interne {self.version}"
                )
                return (True, version_bdd)
        print(
            f"Version de la bdd : {version_bdd}\nVersion de l'appli en interne {self.version}"
        )
        version_bdd_plus_recente = liste_version_bdd[0][0]
        return (False, version_bdd_plus_recente)

    def requete_connexion(self, identifiant: str, mdp) -> tuple:
        """Effectue la requette permettant la verificaton de la connexion

        Args:
            identifiant (str): identifiant rentre par l'utilisateur dans l'ihm
            mdp (_type_): mot de passe rentre par l'utilisateur dans l'ihm

        Returns:
            renvoie un tuple (bool, )
            si la connection est autorisee, renvoi (True , id de l'utilisateur dans la bdd)
            si la connexion est refusee, renvoi (False, "Erreur d'identification") ou (False, "Identifiant inconnu")
        """

        # requete à la bdd
        requete = (
            "select mdp, idUtilisateur from [dbo].[UTILISATEUR] WHERE identifiant = ?;"
        )
        objRequete = Requete(requete, identifiant)
        resultat = self.executerRequete(objRequete, True)

        if (
            len(resultat) != 0
        ):  # on verifie si la reponse n'est pas vide, donc si l'identifiant est valide
            for ligne in resultat:
                if len(mdp) != 0 and bcrypt.checkpw(mdp.encode("utf-8"), ligne[0]):
                    # connexion autorisee
                    idUtilisateur = ligne[1]
                    return (True, idUtilisateur)
                else:
                    return (False, "Erreur d'identification")
        else:
            return (False, "Identifiant inconnu")

    def caracteres_speciaux(self, chaine):
        liste_speciale = [
            "A",
            "I",
            "O",
            "U",
            "C",
            "E",
            "É",
            "Á",
            "Ó",
            "È",
            "À",
            "Ò",
            "Ê",
            "Â",
            "Ô",
            "Ë",
            "Ç",
            "Ñ",
            "Î",
            "Ï",
            "Û",
            "Ü",
            "Ù",
            "Í",
            "Ö",
            "Ä",
            "é",
            "á",
            "ó",
            "è",
            "à",
            "ò",
            "ê",
            "â",
            "ô",
            "ë",
            "ç",
            "ñ",
            "î",
            "ï",
            "û",
            "ü",
            "ù",
            "í",
            "ä",
            "ö",
            "a",
            "e",
            "i",
            "o",
            "u",
            "c",
        ]
        new_chaine = ""

        for caractere in chaine:
            if caractere in liste_speciale:
                new_chaine += "_"
            else:
                new_chaine += caractere

        return new_chaine

    def requeteRechercher(self, frame) -> list:
        """Effectue la requete de Recherche de nom et images vers la bdd.
        Recupere toutes les informations de la frame qui ont ete saisies par l'utilisateur
        Traitement des donnees  et construction de la requetes et de ses conditions
        Execution de la requete pour Obtenir les NOMS et IMAGES correspondants aux parametres

        Args:
            frame (ctk.CTkScrollableFrame: frame recehrche qui appelle cette fonction

        Returns:
            list: Reponse de la bdd sous la fomre liste de tuples [(nom1,image1),(nom3,image2),...]
        """

        # construction de differentes conditions de la requete à partir des informations saisies par l'utilisateur dans la frame
        listeConditions = (
            []
        )  # liste des conditions qui vont etre integrees dans la requete
        tupleParametres = ()

        # ajout condition de jointure table Favoris et plat
        tupleParametres += (obtenirIdUtilisateur(),)

        if frame.recherche != "":
            listeConditions.append("nom like ? ")
            tupleParametres += (f"%{self.caracteres_speciaux(frame.recherche)}%",)
        if frame.typeRepas != "Non Renseigné":
            listeConditions.append("typeRepas = ? ")
            tupleParametres += (frame.typeRepas,)
        if frame.typePlat != "Non Renseigné":
            listeConditions.append("typePlat = ?  ")
            tupleParametres += (frame.typePlat,)
        if frame.typeSaison != "Toutes":
            listeConditions.append("saison = ? ")
            tupleParametres += (frame.typeSaison,)
        if frame.preparation != "off":
            listeConditions.append("tempsPreparation <= ?  ")
            tupleParametres += (
                str(self.miseEnFormeTIME(frame.tpsPrepaH, frame.tpsPrepaMin)),
            )
        if frame.cuisson != "off":
            listeConditions.append("(tempsCuisson <= ? OR tempsCuisson IS NULL) ")
            tupleParametres += (
                str(self.miseEnFormeTIME(frame.tpsCuissonH, frame.tpsCuissonMin)),
            )
        if frame.auteur != "Tous":
            listeConditions.append("auteur = ? ")
            tupleParametres += (frame.auteur,)
        # pour les ustensiles :
        for ustensile in frame.ustensiles:
            listeConditions.append(" (ustensile NOT LIKE ? OR ustensile IS NULL) ")
            tupleParametres += (f"%{ustensile}%",)

        # pout les favoris:
        if frame.favoris == "Favoris":
            listeConditions.append("note >= 6")
        elif frame.favoris == "Recettes sans note":
            listeConditions.append(" note IS NULL ")
        if (
            frame.aleatoire == 1
        ):  # lors de la recherche aleatoire, on ne propose pas les plats avec une note de 0
            listeConditions.append("note != 0 OR note IS NULL")

        # construction des conditions en str a partir de listeConditions
        conditions = ""
        for condition in listeConditions:
            conditions += condition + " AND "

        # enlever le dernier AND
        if conditions != "":
            conditions = "WHERE " + conditions[:-4]

        # Classer les resultats de la recherche
        if frame.classement == "Nom":
            classement = " ORDER BY nom ASC"
        else:
            classement = " ORDER BY COALESCE(f.note, -1) DESC, nom ASC"

        # Requete à la bdd
        requete = (
            "SELECT nom, photoBin, p.idPlat from [dbo].[PLAT] p LEFT JOIN [dbo].[FAVORIS] f ON p.idPlat = f.idPlat AND f.idUtilisateur= ?  "
            + conditions
            + classement
            + ";"
        )
        objRequete = Requete(requete, tupleParametres)
        resultat = self.executerRequete(objRequete, True)

        return resultat

    def requeteRecupererTousUtilisateurs(self) -> list:
        """Permet de recuperer tous les identifiants des utilisateurs"""
        listeIdentifiant = []

        objReq = Requete("SELECT identifiant FROM [dbo].[UTILISATEUR] ;")
        resultat = self.executerRequete(objReq, True, False)
        for ligne in resultat:
            listeIdentifiant.append(ligne[0])

        return listeIdentifiant

    # def requeteAfficherRecette(self, nomRecette: str) -> tuple:
    #     """Effectue la requete vers la bdd pour obtenir toutes les informations d'une recette donnee.
    #     Execution de la requete pour toutes les colones correspondant a la recette dont le nom est passe en parametre

    #     Args:
    #         nomRecette (str): Nom de la recette dont on veut recuperer les infos

    #     Returns:
    #         tuple: contient toutes les infos demmandees
    #     """
    #     # requete à la bdd
    #     requete = "SELECT * from [dbo].[PLAT] WHERE nom= ? ;"
    #     objReq = Requete(requete, nomRecette)
    #     resultat = self.executerRequete(objReq, True)
    #     return resultat[0]

    def requeteAfficherRecetteParID(self, idPlat: str) -> tuple:
        """Effectue la requete vers la bdd pour obtenir toutes les informations d'une recette donnee.
        Execution de la requete pour toutes les colones correspondant a la recette dont l'id' est passe en parametre

        Args:
            nomRecette (str): Nom de la recette dont on veut recuperer les infos

        Returns:
            tuple: contient toutes les infos demmandees
        """
        # requete à la bdd
        requete = "SELECT * from [dbo].[PLAT] WHERE idPlat= ? ;"
        objReq = Requete(requete, idPlat)
        resultat = self.executerRequete(objReq, True)
        return resultat[0]

    def requeteObtenirNoteFavoris(self, idPlat: str) -> int:
        """Permet d'obtenir la note mise à une recette dans la table favoris

        Args:
            idPlat (str): id du plat dans la bdd

        Returns:
            int: note du favoris. Renvoie None si aucun favoris n'existe
        """
        requete = (
            "SELECT note FROM [dbo].[FAVORIS] where idPlat = ? and idUtilisateur = ? ; "
        )
        objReq = Requete(requete, (idPlat, obtenirIdUtilisateur()))
        resultat = self.executerRequete(objReq, True)
        if (
            len(resultat) != 0
        ):  # on verifie si la reponse n'est pas vide, donc si l'utilsateur a deja entre ce plat en favoris
            return resultat[0][0]
        else:  # si ce plat n'est pas associe a l'utilsateur dans la table favoris
            return None

    def requeteAjoutFavoris(self, idPlat: str, note: int):
        """Permet d'ajouter un favoris ou d'en modifier un existant pour une recette donnee

        Args:
            idPlat (str): id du plat a mettre en favoris
            note (int): note a mettre
        """
        verifFavoris = self.requeteObtenirNoteFavoris(idPlat)

        if (
            verifFavoris == None
        ):  # il n'y a pas encore de ligne favoris, on ajoute une ligne
            requete = "INSERT INTO [dbo].[FAVORIS] (idPlat, idUtilisateur, dateDerniereUtilisation, note) VALUES (?, ?, ?, ?) ; "
            objRequete = Requete(
                requete, (idPlat, obtenirIdUtilisateur(), date.today(), note)
            )
            self.executerRequete(objRequete)

        else:  # si il y a deja une ligne favoris, on la modifie
            requete = "UPDATE [dbo].[FAVORIS] SET dateDerniereUtilisation = ?, note = ? WHERE idPlat = ? AND idUtilisateur= ? ;"
            objRequete = Requete(
                requete, (date.today(), note, idPlat, obtenirIdUtilisateur())
            )
            self.executerRequete(objRequete)

        print("Le Favoris a été ajouté")

    def requeteModifierRecette(
        self,
        idPlat_initial,
        nomRecette_initial,
        recette_initial,
        typeRepas_initial,
        typePlat_initial,
        saison_initial,
        difficulte_initial,
        tpsPrepa_initial,
        tpsCuisson_initial,
        nbreParts_initial,
        ustensiles_initial,
        source_initial,
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
        cheminImage,
    ):
        # Verifier les contraintes sur le nom et la recette
        resultatVerification = self.verificationContraiteRecette(
            nomRecette, recette, idPlat_initial, True
        )
        if resultatVerification != True:
            return resultatVerification

        # Si la verification est conforme
        tpsPrepa = str(self.miseEnFormeTIME(tpsPrepaH, tpsPrepaMin))

        tupleParametres = ()
        listeChamps = []

        valeurs_initiales = [
            nomRecette_initial,
            recette_initial,
            typeRepas_initial,
            saison_initial,
            difficulte_initial,
            tpsPrepa_initial,
            nbreParts_initial,
            ustensiles_initial,
            source_initial,
        ]
        valeurs_modifiées = [
            nomRecette.replace("\n\n", "\n"),
            recette.replace("\n\n", "\n"),
            typeRepas,
            typeSaison,
            difficulte,
            tpsPrepa,
            nombreParts,
            ustensiles,
            source,
        ]
        noms_colonnes = [
            "nom",
            "recette",
            "typeRepas",
            "saison",
            "difficulte",
            "tempsPreparation",
            "nombreParts",
            "ustensile",
            "source",
        ]
        for nomColone, valInit, valModif in zip(
            noms_colonnes, valeurs_initiales, valeurs_modifiées
        ):
            if str(valInit) != str(valModif):
                tupleParametres += (valModif,)
                listeChamps.append(nomColone)

        tpsCuisson = self.miseEnFormeTIME(tpsCuissonH, tpsCuissonMin)
        if cuisson == "off" and tpsCuisson_initial is not None:
            tupleParametres += (None,)
            listeChamps.append("tempsCuisson")
        elif cuisson == "on":
            if tpsCuisson_initial != tpsCuisson:
                tupleParametres += (str(tpsCuisson),)
                listeChamps.append("tempsCuisson")
        if typePlat == "Non Renseigné" and typePlat_initial is not None:
            tupleParametres += (None,)
            listeChamps.append("typePlat")
        elif typePlat != "Non Renseigné":
            if typePlat != typePlat_initial:
                tupleParametres += (typePlat,)
                listeChamps.append("typePlat")

        if cheminImage != None:
            with open(cheminImage, "rb") as file:
                binaryData = file.read()

                tupleParametres += (binaryData,)
                listeChamps.append("photoBin")
        # verification qu'une modification a bien eu lieu:
        if len(tupleParametres) == 0:
            return True

        champs = ""
        for champ in listeChamps:
            champs += champ + " = ?, "
        champs = champs[:-2]

        tupleParametres += (idPlat_initial,)

        # requete à la bdd
        requeteModification = "UPDATE [dbo].[PLAT] SET " + champs + " WHERE idPlat =? ;"
        objReqModif = Requete(requeteModification, tupleParametres)
        resultat = self.executerRequete(objReqModif)
        return True

    def verificationContraiteRecette(
        self,
        nomRecette: str,
        recette: str,
        idPlat: str = None,
        modification: bool = False,
    ):
        """effectue les verifications necessaires en terme d'unicité et de taille sur le nom de la recette et la recette
        Mettre modification a True si on effectue la verification dan sle cadre d'une modification de recette. Dans ce cas, présiser aussi idPlat
        return True si le nom de la recette et la recette sont conformes
        return l'erreur sinon
        """
        # contrainte sur le nom de la recette et la saisie
        if len(recette) == 1 and (len(nomRecette) == 0 or len(nomRecette) > 990):
            return "Tout_Faux"

        # contrainte sur le nom de la recette
        elif len(nomRecette) == 0 or len(nomRecette) > 990:
            return "Faux_nom"

        # contrainte sur la saisie de la recette
        elif len(recette) == 1:
            return "Faux_recette"

        # Veriffier que le nom de la recette est unique
        if modification:
            requete = "SELECT nom FROM [dbo].[PLAT] WHERE nom LIKE ? AND idPlat != ?;"
            objRequete_nom = Requete(requete, (nomRecette, idPlat))
        else:
            requete = "SELECT nom FROM [dbo].[PLAT] WHERE nom LIKE ? ;"
            objRequete_nom = Requete(requete, nomRecette)
        resultat_nom = self.executerRequete(objRequete_nom, True)
        if len(resultat_nom) != 0:
            return "Faux_nom"

        return True

    def requeteAjoutRecette(
        self,
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
        cheminImage,
    ):
        tpsPrepa = ""
        tpsCuisson = ""

        # Verifier les contraintes sur le nom et la recette
        resultatVerification = self.verificationContraiteRecette(nomRecette, recette)
        if resultatVerification != True:
            return resultatVerification

        # Si la verification est conforme
        tpsPrepa = str(self.miseEnFormeTIME(tpsPrepaH, tpsPrepaMin))
        # obtenir la date actuelle
        date_now = date.today()

        tupleParametres = (
            nomRecette,
            recette,
            typeRepas,
            typeSaison,
            difficulte,
            tpsPrepa,
            nombreParts,
            ustensiles,
            obtenirIdentifiantUtilisateur(),
            source,
            date_now,
        )
        listeChamps = [
            "nom",
            "recette",
            "typeRepas",
            "saison",
            "difficulte",
            "tempsPreparation",
            "nombreParts",
            "ustensile",
            "auteur",
            "source",
            "dateCreation",
        ]

        if cuisson == "on":
            tupleParametres += (str(self.miseEnFormeTIME(tpsCuissonH, tpsCuissonMin)),)
            listeChamps.append("tempsCuisson")

        if typePlat != "Non Renseigné":
            tupleParametres += (typePlat,)
            listeChamps.append("typePlat")

        if cheminImage != None:
            with open(cheminImage, "rb") as file:
                binaryData = file.read()

                tupleParametres += (binaryData,)
                listeChamps.append("photoBin")

        champs = ""
        for champ in listeChamps:
            champs += champ + ","
        champs = champs[:-1]

        pointsInterrogation = "? ," * len(tupleParametres)
        pointsInterrogation = pointsInterrogation[:-1]

        # requete à la bdd
        requeteAjout = (
            "INSERT INTO [dbo].[PLAT] ("
            + champs
            + ") VALUES ("
            + pointsInterrogation
            + ");"
        )
        objReqAjout = Requete(requeteAjout, tupleParametres)
        resultat = self.executerRequete(objReqAjout)

        return True

    def suppression_compte(self, idUtilisateur, identifiant: str):
        """Execute toutes les requetes permettant la suppresion du compte lie a l'idUtilisateur et l'anonymisation des recettes

        Args:
            idUtilisateur (_type_): _description_
            identifiant
        """
        # requete à la bdd

        requete = "DELETE FROM [dbo].[FAVORIS] WHERE idUtilisateur = ?;UPDATE [dbo].[PLAT] SET auteur = 'un ancien utilisateur' WHERE auteur = ?;DELETE FROM [dbo].[UTILISATEUR] WHERE idUtilisateur = ?;"
        objReq = Requete(requete, (idUtilisateur, identifiant, idUtilisateur))
        self.executerRequete(objReq)

    def nb_recettes(self):
        """
        Retourne le nombre de recettes presentes au total dans la bdd
        """
        nbreRecette = 0

        requete = "SELECT COUNT(*) FROM [dbo].[PLAT];"
        objRequete = Requete(requete)
        resultat = self.executerRequete(objRequete, True, False)

        for ligne in resultat:
            nbreRecette = ligne[0]

        return nbreRecette

    def nb_recettes_perso(self):
        """
        Retourne le nombre de recettes de l'utilisateur dans la bdd
        """
        nbreRecette = 0

        requete = "SELECT COUNT(*) FROM [dbo].[PLAT] WHERE auteur=?;"
        objRequete = Requete(requete, obtenirIdentifiantUtilisateur())
        resultat = self.executerRequete(objRequete, True, False)

        for ligne in resultat:
            nbreRecette = ligne[0]

        return nbreRecette

    def nb_utilisateurs(self):
        """
        Retourne le nombre d'utilisateurs inscrits dans la bdd
        """
        nbreUtilisateur = 0

        requete = "SELECT COUNT(*) FROM [dbo].[UTILISATEUR];"
        objRequete = Requete(requete)
        resultat = self.executerRequete(objRequete, True, False)

        for ligne in resultat:
            nbreUtilisateur = ligne[0]

        return nbreUtilisateur

    def requeteUniciteUtilisateur(self):
        """
        Renvoi Tous les identifiant et mail de la bdd
        """

        requete = "SELECT identifiant, mail FROM [dbo].[UTILISATEUR];"
        objRequete = Requete(requete)
        result = self.executerRequete(objRequete, True)
        return result

    def requeteAjoutUtilisateur(self, mdp, identifiant, mailSecurise):
        """Requete qui permet d'ajouter un utilisateur dans la bdd avec un mot de passe , identifiant et mail

        Args:
            mdp (_type_): _description_
            identifiant (_type_): _description_
            mailSecurise (_type_): _description_
        """
        mdpHased = bcrypt.hashpw(mdp.encode("utf-8"), bcrypt.gensalt())

        # requete à la bdd
        objReq = Requete(
            "INSERT INTO [dbo].[UTILISATEUR] (identifiant, mdp, mail) VALUES (?, ?, ?)",
            (identifiant, mdpHased, mailSecurise),
        )
        self.executerRequete(objReq, False)

    def requeteModifierMdp(self, nouveauMpd_bc, identifiant):
        # ouverture de la connection à la bdd

        requete = "UPDATE [dbo].[UTILISATEUR] SET mdp = ? WHERE identifiant = ?;"

        objRequete = Requete(requete, (nouveauMpd_bc, identifiant))
        self.executerRequete(objRequete)

    def requeteEnvoyerMail(self, framePbConnexion, mail):
        # verification du mail:
        objReq_1 = Requete("SELECT mail FROM [dbo].[UTILISATEUR] ;")
        resultat_1 = self.executerRequete(objReq_1, True)

        verif_mail = False
        for ligne in resultat_1:
            if desecuriserMail(ligne[0]) == mail:
                verif_mail = True
                hashMailBDD = ligne[0]
                break

        # Si le mail est valide
        if verif_mail == True:
            # requete à la bdd
            requete_2 = "SELECT identifiant FROM [dbo].[UTILISATEUR] where mail =? ;"
            objReq_2 = Requete(requete_2, (hashMailBDD,))
            rows = self.executerRequete(objReq_2, True)

            for ligne in rows:
                # generer un nouveau mdp aleatoire
                caractere = string.ascii_letters + string.digits + string.punctuation
                new_mdp = "".join(random.choice(caractere) for _ in range(10))

                print("envoi du mail")
                envoyerMail(mail, new_mdp, ligne[0])

                # modification du mdp dans la BDD
                requete_3 = (
                    "UPDATE [dbo].[UTILISATEUR] SET mdp = ? WHERE identifiant = ?;"
                )
                new_mdp_bc = bcrypt.hashpw(new_mdp.encode("utf-8"), bcrypt.gensalt())

                objReq_3 = Requete(requete_3, (new_mdp_bc, str(ligne[0])))
                self.executerRequete(objReq_3)

                framePbConnexion.texte_PBconnexion.configure(
                    font=("Times New Roman", 16, "bold"),
                    text_color="DeepSkyBlue1",
                    text="Mail Envoyé",
                )

        else:
            framePbConnexion.texte_PBconnexion.configure(
                font=("Times New Roman", 16, "bold"),
                text_color="red",
                text="Mail Inconnu",
            )

    def executerRequete(
        self,
        objetRequete: Requete,
        retournerLignes: bool = False,
        afficherMessage: bool = True,
    ):
        try:
            if afficherMessage:
                self.fenetre.effacerInformation()
            resultat_requete = objetRequete.executer(
                self.connect_string, retournerLignes
            )
            return resultat_requete

        except Exception as e:
            print("###########ERREUR##################")
            print("Une erreur est survenue : ", e)
            print("###################################")
            if afficherMessage:
                self.fenetre.afficherInformation(
                    "Un problème est survenu.\n Auncune opération \n ne peut aboutir.\n (Verifiez que vous êtes\n connecté à Internet)"
                )


def envoyerMail(mail: str, new_mdp, identifiant):
    """Permet d'envoyer un mail contenant un nouveau mdp associe a un identifiant"""
    # envoie du mail avec les nouveaux identifiants
    adresse_expediteur = mail_adresse_expediteur
    adresse_destinataire = str(mail)  # à modifier si nécessaire
    sujet = "Une Petite Faim: Oubli de vos identifiants"
    corps = (
        "Bonjour cher client(e).\n\nNous vous informons d'une demande d'identifiants.\nIdentifiant : "
        + str(identifiant)
        + "\nNouveau Mot de Passe : "
        + str(new_mdp)
        + " (vous pourrez le modifier à tout moment) \nÀ vos fourneaux \U0001F382  \U0001F600 . \nCordialement, le service client.\n\n\nCe mail est un message automatique.\nPour des renseignements complémentaires, merci de contacter le service client à cette adresse : unepetitefaim.mb.ap@gmail.com "
    )

    # Créer un objet EmailMessage
    message = EmailMessage()
    message["From"] = adresse_expediteur
    message["To"] = adresse_destinataire
    message["Subject"] = sujet
    message.set_content(corps)

    # Paramètres du serveur SMTP d'Outlook.com
    serveur_smtp = "smtp-mail.outlook.com"
    port_smtp = 587

    # Établir une connexion sécurisée SMTP avec TLS
    contexte = ssl.create_default_context()
    with smtplib.SMTP(serveur_smtp, port_smtp) as smtp_objet:
        smtp_objet.starttls(context=contexte)

        # Authentification
        smtp_objet.login(adresse_expediteur, mail_mot_de_passe)

        # Envoyer l'e-mail
        smtp_objet.send_message(message)

        # Fermer la connexion SMTP
        smtp_objet.quit()
