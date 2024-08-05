import numpy as np
import time

class Courbe(object):
    """ Classe generique definissant une courbe. """
    
    def __init__(self, num_click = 4, points = []):
        self.controles = []
        self.yes_no = True
        self.num_click = num_click
        self.points = points

    def dessinerControles(self, dessinerControle, color):
        """ Dessine les points de controle de la courbe. """
        for controle in self.controles:
            dessinerControle(controle, color)

    def dessinerPoints(self, dessinerPoint):
        """ Dessine la courbe. Methode a redefinir dans les classes derivees. """
        pass

    def ajouterControle(self, point):
        """ Ajoute un point de controle. """
        print(point)
        self.controles.append(point)
    
    def deplacer(self, new_position):
        """ Change la courbe """
        dessinerPoints(self, new_position)


    
        

        
class Horizontale(Courbe):
    """ Definit une horizontale. Derive de Courbe. """                  
                
    def ajouterControle(self, point):
        """ Ajoute un point de controle a l'horizontale.
        Ne fait rien si les 2 points existent deja. """
        if len(self.controles) < 2:
            Courbe.ajouterControle(self, point)

    def dessinerPoints(self, dessinerPoint):
        """ Dessine la courbe. Redefinit la methode de la classe mere. """
        if len(self.controles) is 2 :
            x1 = self.controles[0][0]
            x2 = self.controles[1][0]
            y = self.controles[0][1]
            xMin = min(x1,x2)
            xMax = max(x1, x2)
            for x in range(xMin, xMax):
                dessinerPoint((x, y))    
   

class nouvelleApprox(Courbe):
    def ajouterControle(self, point):
        """ Ajoute un point de controle a l'horizontale.
        Ne fait rien si les 2 points existent deja. """
        if len(self.controles) < self.num_click:
            Courbe.ajouterControle(self, point)
            
    def dessinerPoints(self, dessinerPoint):
        """ Approximer 4 points par une courbe """
        if len(self.controles) is self.num_click :
            x = np.zeros((self.num_click))
            y = np.zeros((self.num_click))
            h = 800
            l = 600
            n = 6
            len_axis_ord = l-2*l//n
            len_axis_abs = h-2*h//n
            
            for j in range(self.num_click):
                temp_x = self.controles[j][0]
                temp_y = self.controles[j][1]
                
                temp_x = (temp_x- h//n)/((n-1)*h//n - h//n )
                temp_y = abs((n-1)*l//n -temp_y)/((n-1)*l//n - l//n )
                
                x[j] = temp_x
                y[j] = temp_y
            
            pol = np.polyfit(x, y, 3)
            ref= np.linspace(0,1, 5000)
            for x in ref:
                Y_abs = x*len_axis_abs//1 + h//n
                h_x = min(1, max(0,pol[0] * np.power(x,3) + pol[1] * np.power(x,2) + pol[2] * x +pol[3]))
                Y_ord = l-(h_x*len_axis_ord//1)- l//n
                dessinerPoint((Y_abs, Y_ord))

class Approx_point_no_limit(Courbe):
    def ajouterControle(self, point):
        """ Ajoute un point de controle a l'horizontale.
        Ne fait rien si les 2 points existent deja. """
        if True:
            Courbe.ajouterControle(self, point)
            
    def dessinerPoints(self, dessinerPoint):
        """ Approximer 4 points par une courbe """
        if len(self.points) >= 2 :
            x = np.zeros((self.num_click))
            y = np.zeros((self.num_click))
            h = 800
            l = 600
            n = 6
            len_axis_ord = l-2*l//n
            len_axis_abs = h-2*h//n
            
            for j in range(self.num_click):
                
                temp_x = self.points[j][0]
                temp_y = self.points[j][1]
                
                temp_x = (temp_x- h//n)/((n-1)*h//n - h//n )
                temp_y = abs((n-1)*l//n -temp_y)/((n-1)*l//n - l//n )
                
                x[j] = temp_x
                y[j] = temp_y
            
            pol = np.polyfit(x, y, 3)
            ref= np.linspace(0,1, 5000)
            for x in ref:
                Y_abs = x*len_axis_abs//1 + h//n
                h_x = min(1, max(0,pol[0] * np.power(x,3) + pol[1] * np.power(x,2) + pol[2] * x +pol[3]))
                Y_ord = l-(h_x*len_axis_ord//1)- l//n
                dessinerPoint((Y_abs, Y_ord))
