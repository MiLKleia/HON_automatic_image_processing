import UI.Modele as Modele
import math


class ControleurCourbes(object):
    """ Gere un ensemble de courbes. """
    def __init__(self):
        self.courbes = []
        self.color = ['blue', 'red', 'green', 'yellow', 'white', 'black', 'purple', 'orange']
        self.display_color=None
        self.incr = 0

    def ajouterCourbe(self, courbe):
        """ Ajoute une courbe supplementaire. 
        Fonction interne. Utiliser plutot nouvelleDroite... """
        self.courbes.append(courbe) 

    def dessiner(self, dessinerControle, dessinerPoint):
        """ Dessine les courbes. """
        self.incr = 0
        # dessine les point de la courbe
        for courbe in self.courbes:
            
            courbe.dessinerPoints(dessinerPoint)
        # dessine les point de controle
        for courbe in self.courbes:
            self.incr = self.incr + 1
            courbe.dessinerControles(dessinerControle, self.color[self.incr%len(self.color)])
    
    def nouvelleHorizontale(self):
        """ Ajoute une nouvelle horizontale initialement vide. 
        Retourne une fonction permettant d'ajouter les points de controle. """
        horizontale = Modele.Horizontale()
        self.ajouterCourbe(horizontale)
        return horizontale.ajouterControle
        
    def nouvelleApprox(self, num_click):
        """ Ajoute une nouvelle  
        Retourne une fonction permettant d'ajouter les points de controle. """
        
        approx = Modele.nouvelleApprox(num_click)
        self.ajouterCourbe(approx)
        return approx.ajouterControle
        
    def saveApprox(self):
        """ Ajoute une nouvelle  
        Retourne une fonction permettant d'ajouter les points de controle. """
        print(self.courbes[-1])
        return 0
        
