import pyodbc
class Requete():
    def __init__(self,requeteStr:str, parametres:tuple=None):
        """_summary_

        Args:
            requeteStr (str): requete SQL sous forme de chaine de caractere avec des '?' a la place de parametres
            parametres (tuple): tuples des parametres de la recette
        """
        self.requeteStr=requeteStr
        self.parametres=parametres
    
    def executer(self,connection_string:str, retournerLignes:bool=False):
        """Execute la requette aupres de la bdd

        Args:
            connexionBDD (sqlite3.Connection): connexion a la bdd, la bdd doit donc etre ouverte au prealable
        """
        with pyodbc.connect(connection_string) as conn:
            with conn.cursor() as cursor:
                if self.parametres is None:
                    resultat=cursor.execute(self.requeteStr)
                else:
                    resultat=cursor.execute(self.requeteStr, self.parametres)

                if retournerLignes:
                    lignes=[]
                    row = cursor.fetchone()
                    while row:
                        lignes.append(row)
                        row = cursor.fetchone()
                    return lignes
                else:
                    return resultat