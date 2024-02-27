#partie en rapport avec l'identifiant et l'id de l'utilisateur qui utilise l'app
identifiantUtilisateur=""
idUtilisateur=0

def modifierIdentifiantEtIdUtilisateur(newId:int,newIdentifiant:str):
    global identifiantUtilisateur, idUtilisateur
    identifiantUtilisateur=newIdentifiant
    idUtilisateur=newId    

def obtenirIdentifiantUtilisateur():
    return identifiantUtilisateur

def obtenirIdUtilisateur():
    return idUtilisateur