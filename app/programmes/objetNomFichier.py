class NomFichier():
    def __init__(self, nomDuFichier:str) -> None:
        self.annee,self.semaine,self.numFichier=nomDuFichier.split("_")[1:]
        self.annee=int(self.annee)
        self.semaine=int(self.semaine)
        self.numFichier=int(self.numFichier)
    

    def getNomFichier(self)->str:
        """renvoie le nom du fichier sous la forme "bdd_annee_semaine_numFichier"

        Returns:
            str: _description_
        """
        
        nomDuFichier=f"bdd_{self.annee}_{mettreNombreSur2Caracteres(self.semaine)}_{mettreNombreSur3Caracteres(self.numFichier)}"
        return nomDuFichier
    
      
    def changerNomFichier(self, anneeActuelle:int, semaineActuelle:int):
        if anneeActuelle!= self.annee or semaineActuelle != self.semaine :
            self.annee = anneeActuelle
            self.semaine=semaineActuelle
            self.numFichier=0
        else:
            self.numFichier+=1

def mettreNombreSur2Caracteres(nombre:int)->str:
        """Transforme un nombre en une chaine de 2 caracteres
        par exemple 1 devient "01" et 12 devient "12" 

        Args:
            nombre (int): _description_

        Returns:
            str: _description_
        """
        nombreStr=str(nombre)
        if len(nombreStr)==1:
            nombreStr="0"+nombreStr
        return nombreStr

def mettreNombreSur3Caracteres(nombre:int)->str:
        """Transforme un nombre en une chaine de 3 caracteres
        par exemple 1 devient "001", 12 devient "012" et 432 devient"432" 

        Args:
            nombre (int): _description_

        Returns:
            str: _description_
        """
        nombreStr=str(nombre)
        if len(nombreStr)==1:
            nombreStr="00"+nombreStr
        elif len(nombreStr)==2:
            nombreStr="0"+nombreStr
        return nombreStr
