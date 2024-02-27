import customtkinter as ctk
from PIL import Image
from functools import partial
import io
from variablesGlobales import cheminDossierData


class FrameApercuRecette(ctk.CTkFrame):
    """Cet objet est une petite frame qui va montrer un apercu d'une recette : son nom et son image
    Elle intervient apres la recherche pour que l'utilisateur puisse choisir qu"elle recette il veut consulter

    La classe FrameApercuRecette herite de la classe ctk.CTkButton
    """

    def __init__(
        self,
        tabView: ctk.CTkTabview,
        frame: ctk.CTkScrollableFrame,
        place: int,
        idPlat: int,
        nomrecette: str,
        imageBinaire: None,
    ):  # methode qui va etre executee a la creation de l'objet
        """
        Args:
            tabView (ctk.CTkTabview): _description_
            frame (ctk.CTkScrollableFrame): frame Scrollable dans l'aquelle va etre integrer cet objet
            place (int): place dans la frame Scrollable verticale pour savoir ou .grid() l'objet
            nomrecette (str): nom de la recette a afficher
            imageBinaire (None): image en binaire de la recette a afficher
        """
        super().__init__(frame, corner_radius=20, fg_color=("black", "white"))
        self.grid_columnconfigure(1, weight=1)
        self.grid(row=place, column=0, sticky="ew", padx=10, pady=10)

        self.tabView = tabView

        tailleImage = 120  # pixels

        # Image Bouton
        if imageBinaire == None:
            my_image = ctk.CTkImage(
                light_image=Image.open(f"{cheminDossierData}/images/ihm/IHMimage.png"),
                size=(tailleImage, tailleImage),
            )
        else:
            img = Image.open(io.BytesIO(imageBinaire))
            width, height = img.size
            my_image = ctk.CTkImage(
                light_image=img, size=(tailleImage, height * tailleImage / width)
            )

        imageButton = ctk.CTkButton(
            self,
            image=my_image,
            text="",
            fg_color="transparent",
            command=partial(self.tabView.creerOngletRecette, idPlat, nomrecette),
        )
        imageButton.grid(row=1, column=1, padx=5, pady=(5, 0))

        # Label nom recette
        self.nomRecetteLabel = ctk.CTkLabel(
            self,
            text=nomrecette,
            fg_color="transparent",
            text_color=("white", "black"),
            wraplength=120,
        )
        self.nomRecetteLabel.grid(row=2, column=1, padx=5, pady=(5, 10))
