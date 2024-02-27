import controleurBDD as ctrlBDD
import os


# Partie en rapport avec la bdd
controleurBDD = False


def creerControleurBDD():
    global controleurBDD
    controleurBDD = ctrlBDD.ControleurBDD()
    """fenetre.controleurTemporaireBDD=ctrlBDD.ControleurBDD()
    fenetre.lancement=True
    return"""


def affecterControleurBDD(ctrl):
    global controleurBDD
    controleurBDD = ctrl


def getControleurBDD():
    return controleurBDD


def definir_chemin_data() -> str:
    """
    renvoie l'emplacement du dossier data parmis une selection
    Si aucun dossier data n'est trouve, provoque une erreur
    """
    directory_paths = ["./_internal/data", "./data", "../data"]
    for path in directory_paths:
        if os.path.exists(path):
            # print(f"Le dossier '{path}' existe.")
            return path
    print(f"Dossier data introuvable. Emplacements tentés : {directory_paths}")
    raise FileNotFoundError(f"Aucun des dossiers '{directory_paths}' existe.")


cheminDossierData = definir_chemin_data()
