# -*- coding: utf-8 -*-
"""
@author: Anthony
"""
from tkinter import *
from tkinter import Tk, Canvas, colorchooser
import tkinter as tk

root = tk.Tk()
root.title("Zone de dessin")


class Point:
    def __init__(self, x, y):  # Définition de la classe Point (composé des variables x et y)
        self.x = x
        self.y = y

    def __str__(self):  # Initialisation des points
        self.P0 = Point(0, 0)
        self.P1 = Point(0, 0)


class Choice:  # Cette class permet de réceptionner le choix de l'utilisateur sur la forme à dessiner
    def __init__(self):
        global choice
        choice = StringVar()
        choice = "Line"

    def choiceCercle():
        global choice
        choice = "Cercle"

    def choiceCarré():
        global choice
        choice = "Carré"

    def choiceOval():
        global choice
        choice = "Oval"

    def choiceLine():
        global choice
        choice = "Line"

    def choiceRectangle():
        global choice
        choice = "Rectangle"

    def choiceTrace():
        global choice
        choice = "Trace"


class MoovSouris:  # Class qui va gérer les différents mouvements de souris en fonction du choix de la forme de l'utilisateur.
    def __init__(self):
        pass

    def clic(self, event):  # Fonction qui gère le 1er clic de l'utilisateur, le point de départ de la forme
        x = event.x
        y = event.y
        self.P0 = Point(x, y)
        if choice == "Cercle":
            Cercle.draw_simplecercle(self, self.P0)
        elif choice == "Carré":
            Carré.draw_simplecarré(self, self.P0)
        elif choice == "Line":
            Line.draw_simple(self, self.P0)
        elif choice == "Oval":
            Oval.draw_simple(self, self.P0)
        elif choice == "Rectangle":
            Rectangle.draw_simple(self, self.P0)

    def modif_clic(self,
                   event):  # Fonction qui gère le mouvement de souris de l'utilisateur afin de déterminer le point final de la forme au moment du relâchement du clic.
        x = event.x
        y = event.y
        self.P1 = Point(x, y)
        if choice == "Cercle":
            Cercle.draw_movecercle(self, self.P0, self.P1)
        elif choice == "Carré":
            Carré.draw_movecarré(self, self.P0, self.P1)
        elif choice == "Line":
            Line.draw_move(self, self.P0, self.P1)
        elif choice == "Oval":
            Oval.draw_move(self, self.P0, self.P1)
        elif choice == "Rectangle":
            Rectangle.draw_move(self, self.P0, self.P1)
        elif choice == "Trace":
            Trace.draw_move(self, self.P0, self.P1)


class Shape:  # Class qui contient le canvas sur lequel les dessins seront faits
    my_canvas = Canvas(root, width=600, height=400, bg="ivory")
    my_canvas.grid(row=0, column=1, rowspan=16, sticky="nsew")

    def __init__(self):
        pass


class effacer(Shape):  # Class qui va effacer les dessins qui ont été faits sur le canvas.
    def __init__(self):
        super().__init__()
        Shape.my_canvas.delete('all')


class Detect(
    Shape):  # Class qui va contenir les fonctions bind permettant de détecter le premier clic de l'utilisateur puis les mouvements avec le clic enfoncer correspondant au premier puis au dernier point respectivement
    def __init__(self):
        super().__init__()

    def press():
        P = MoovSouris()
        Shape.my_canvas.bind("<ButtonPress-1>", P.clic)  # pour le premier clic
        Shape.my_canvas.bind("<B1-Motion>", P.modif_clic)  # pour le déplacement bouton enfoncé


class Choose_color_line:  # # Permet d'initialiser la couleur des contours de chacune des formes. Définis comme variable globale, car je n'ai pas réussi à utiliser l'héritage pour transférer la variable du choix de la couleur tout en ayant des couleurs "par défault" au cas où l'utilisateur ne choisirait pas.
    global colorhex_line
    colorhex_line = '#a0a0a0'  # Couleur du contour par défault

    def color_line():
        global colorhex_line
        color_code = colorchooser.askcolor(
            title="Choose color")  # Utilisation du module askcolor pour choisir une couleur à l'utilisateur et la renvoyer au programme.
        colorhex_line = color_code[1]  # On isole la couleur choisie par l'utilisateur sous forme de code hexadécimale.


class Choose_color_remp:  # Permet d'initialiser la couleur du remplissage de chacune des formes. Définis comme variable globale, car je n'ai pas réussi à utiliser l'héritage pour transférer la variable du choix de la couleur tout en ayant des couleurs "par défault" au cas où l'utilisateur ne choisirait pas.
    global colorhex_remp
    colorhex_remp = "ivory"  # Couleur du remplissage par défault

    def color_remp():
        global colorhex_remp
        color_code = colorchooser.askcolor(
            title="Choose color")  # Utilisation du module askcolor pour choisir une couleur à l'utilisateur et la renvoyer au programme.
        colorhex_remp = color_code[1]  # On isole la couleur choisie par l'utilisateur sous forme de code hexadécimale.

    def color_transp():
        global colorhex_remp
        colorhex_remp = ""  # Une variable String vide ('') indique : transparence


class Oval(Shape):  # Class qui contient les fonction canvas pour créer des Ovales et qui hérite de "Shape" qui apporte le lien avec la zone de dessin.
    def __init__(self):
        super().__init__()

    def draw_simple(self, P0):  # Fonction qui reçoit seulement le premier point (P0), qui va créer un premier Oval qui ne sera défini que par son premier point et qui ne sera pas affiché.
        self.item = Shape.my_canvas.create_oval(P0.x, P0.y, P0.x, P0.y, fill=colorhex_remp, outline=colorhex_line)
        return self.item

    def draw_move(self, P0, P1):  # Fonction qui reçoit le premier point (P0) et le dernier point (P1). Cette fonction va utiliser et afficher le canvas Oval créé précédemment en ayant modifié ces coordonnées en prenant en compte le premier point (P0) et le dernier point (P1) sachant que le dernier point sera mis à jour à chaque mouvement de la souris de l'utilisateur tant que le clic gauche est enfoncé.
        Shape.my_canvas.coords(self.item, P0.x, P0.y, P1.x, P1.y)


class Cercle(Oval):  # Class qui hérite de "Oval" ce qui permet à la class Cercle d'utiliser les fonctions de dessin de la class Oval.
    def __init__(self):
        super().__init__(self)

    def draw_simplecercle(self, P0):  # Fonction qui reçoit seulement le premier point (P0), et qui va utiliser la fonction "draw_simple" de la class Oval pour créer ça propre forme "oval" qui ne sera pas affiché.
        self.item = Oval.draw_simple(self, P0)

    def draw_movecercle(self, P0, P1):  # Fonction qui reçoit le premier point (P0) et le dernier point (P1). Cette fonction va utiliser la fonction "draw_move" de la class Oval. Il va utiliser la forme oval créée précédemment et modifier ces coordonnées en prenant en compte le premier point (P0) et le dernier point (P1). Avant cela, le dernier point sera modifié afin de toujours afficher un cercle.
        diam = ((P0.x - P1.x) ** 2 + (P0.y - P1.y) ** 2) ** 0.5
        P1 = Point(P0.x + diam, P0.y + diam)
        Oval.draw_move(self, P0, P1)


class Line(Shape):  # Class qui contient les fonction canvas pour créer des Lignes et qui hérite de "Shape" qui apporte le lien avec la zone de dessin.
    def __init__(self):
        super().__init__()

    def draw_simple(self, P0):  # Fonction qui reçoit seulement le premier point (P0), qui va créer une première Line qui ne sera défini que par son premier point et qui ne sera pas affiché.
        self.item = Shape.my_canvas.create_line(P0.x, P0.y, P0.x, P0.y, fill=colorhex_line)

    def draw_move(self, P0, P1):  # Fonction qui reçoit le premier point (P0) et le dernier point (P1). Cette fonction va utiliser et afficher le canvas Line créé précédemment en ayant modifié ces coordonnées en prenant en compte le premier point (P0) et le dernier point (P1) sachant que le dernier point sera mis à jour à chaque mouvement de la souris de l'utilisateur tant que le clic gauche est enfoncé.
        Shape.my_canvas.coords(self.item, P0.x, P0.y, P1.x, P1.y)


class Rectangle(Shape):  # Class qui contient les fonction canvas pour créer des Rectangles et qui hérite de "Shape" qui apporte le lien avec la zone de dessin.
    def __init__(self):
        super().__init__()

    def draw_simple(self, P0):  # Fonction qui reçoit seulement le premier point (P0), qui va créer un premier Rectangle qui ne sera défini que par son premier point et qui ne sera pas affiché.
        self.item = Shape.my_canvas.create_rectangle(P0.x, P0.y, P0.x, P0.y, fill=colorhex_remp, outline=colorhex_line)
        return self.item

    def draw_move(self, P0, P1):  # Fonction qui reçoit le premier point (P0) et le dernier point (P1). Cette fonction va utiliser et afficher le canvas Rectangle créé précédemment en ayant modifié ces coordonnées en prenant en compte le premier point (P0) et le dernier point (P1) sachant que le dernier point sera mis à jour à chaque mouvement de la souris de l'utilisateur tant que le clic gauche est enfoncé.
        Shape.my_canvas.coords(self.item, P0.x, P0.y, P1.x, P1.y)


class Carré(Rectangle):  # Class qui hérite de "Rectangle" ce qui permet à la class Carrée d'utiliser les fonctions de dessin de la class Rectangle.
    def __init__(self):
        super().__init__(self)

    def draw_simplecarré(self, P0):  # Fonction qui reçoit seulement le premier point (P0), et qui va utiliser la fonction "draw_simple" de la class Rectangle pour créer ça propre forme "rectangle" qui ne sera pas affiché.
        self.item = Rectangle.draw_simple(self, P0)

    def draw_movecarré(self, P0, P1):  # Fonction qui reçoit le premier point (P0) et le dernier point (P1). Cette fonction va utiliser la fonction "draw_move" de la class Rectangle. Il va utiliser la forme rectangle créée précédemment et modifier ces coordonnées en prenant en compte le premier point (P0) et le dernier point (P1). Avant cela, le dernier point sera modifié afin de toujours afficher un carré.
        diam = ((P0.x - P1.x) ** 2 + (P0.y - P1.y) ** 2) ** 0.5
        P1 = Point(P0.x + diam, P0.y + diam)
        Rectangle.draw_move(self, P0, P1)


class Trace(Shape):  # Class qui contient les fonction canvas pour créer des dessins à main levée et qui hérite de "Shape" qui apporte le lien avec la zone de dessin.
    def __init__(self):
        super().__init__()

    def draw_move(self, P0, P1):  # Fonction qui reçoit le premier point (P0) et le dernier point (P1). Cette fonction va créer un point à chaque mouvement de la souris avec le clic enfoncé et modifier le point de départ de la forme pour qu'il suive les mouvements. Permet un dessin à main levé sans forme prédéfinit.
        Shape.my_canvas.create_line(P0.x, P0.y, P1.x, P1.y, fill=colorhex_line)
        P0.x, P0.y = P1.x, P1.y


##----- Création des bouton et zone de textes de l'affichage -----##
labelforme = Label(root, text='Formes: ')

buttoncercle = Button(root, text="Cercle : ◯", command=Choice.choiceCercle)
buttoncarré = Button(root, text="Carré : ◻", command=Choice.choiceCarré)
buttonoval = Button(root, text="Ovale : ⬯", command=Choice.choiceOval)
buttondroite = Button(root, text="Ligne :  /", command=Choice.choiceLine)
buttonrectangle = Button(root, text="Rectangle : ▭", command=Choice.choiceRectangle)
buttontrace = Button(root, text="Trace : ⱴ", command=Choice.choiceTrace)

labelcouleur = Label(root, text='Couleurs : ')
buttoncouleur = Button(root, text="Def", command=Choose_color_line.color_line)

labelremplissage = Label(root, text='Remplissage : ')
buttonremplissage = Button(root, text="Def", command=Choose_color_remp.color_remp)
buttontransparent = Button(root, text="Transparent", command=Choose_color_remp.color_transp)

labelvide = Label(root, text='')
buttondelete = Button(root, text="Effacer", command=effacer)

##----- Affichage des bouton et zone de textes de l'affichage -----##
labelforme.grid(row=0, column=0, sticky="nsew")

buttoncercle.grid(row=1, column=0, sticky="nsew")
buttoncarré.grid(row=2, column=0, sticky="nsew")
buttonoval.grid(row=3, column=0, sticky="nsew")
buttondroite.grid(row=4, column=0, sticky="nsew")
buttonrectangle.grid(row=5, column=0, sticky="nsew")
buttontrace.grid(row=6, column=0, sticky="nsew")

labelcouleur.grid(row=8, column=0, sticky="nsew")
buttoncouleur.grid(row=9, column=0, sticky="nsew")

labelremplissage.grid(row=11, column=0, sticky="nsew")
buttonremplissage.grid(row=12, column=0, sticky="nsew")
buttontransparent.grid(row=13, column=0, sticky="nsew")

labelvide.grid(row=14, column=0, sticky="nsew")
buttondelete.grid(row=15, column=0, sticky="nsew")

##----- Programme principal -----##
Shape()  # Appel la class "Shape" qui va afficher la zone de dessin (canvas)
Detect.press()  # Appel la class "Detect" qui va lancer les fonction bind qui détecte les clic sur la zone de dessin (canvas).
Choice()  # Appel la class "Choice" qui va définir "Line" comme forme par défaut tant qu'aucune class n'a été choisie par l'utilisateur.

root.mainloop()
