import tkinter 
from PIL import ImageTk, Image, ImageDraw
import UI.Controleur as Controleur




class EtalFunction(object):
    def __init__(self, largeur, hauteur):
        self.controleur = Controleur.ControleurCourbes()
        self.largeur = largeur
        self.hauteur = hauteur
        self.n = 6
        self.canvas = []
        self.image = []
        self.imageDraw = []
        self.imageTk = []
        self.outilsCourant = []  
        self.selected_point_index = None
        self.last_mouse_position = None 
        self.all_points = []
        self.dark = False
        self.num_click = 4
        
         
    def callbackButton1(self, event):
        """ Bouton gauche : utilise l'outils courant. """
        if self.outilsCourant:
            self.outilsCourant((event.x, event.y))
            self.all_points.append([event.x, event.y])
        self.majAffichage()
        
    def callbackButton3(self, event):
        """ Bouton droit : termine l'outils courant et déselectionne le point. """
        self.outilsCourant = None
        self.selected_point_index = None
        self.last_mouse_position = None
        self.majAffichage()
        
    def callbackNouveau(self):
        """ Supprime toutes les courbes. """
        self.controleur = Controleur.ControleurCourbes()
        self.majAffichage()
        self.all_points = []
        
    def majAffichage(self):
        """ Met a jour l'affichage.. """
        self.imageDraw.rectangle([0, 0, self.largeur, self.hauteur], fill='lightgrey')
        fonctionPoint = lambda p: self.imageDraw.point(p, (0, 0, 0))
        fonctionControle = lambda p, color: self.imageDraw.rectangle([p[0] - 3,
                        p[1] - 3, p[0] + 3, p[1] + 3], fill=color)
        self.controleur.dessiner(fonctionControle, fonctionPoint)
        self.imageTk = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(self.largeur/2 + 1, self.hauteur/2 + 1, image=self.imageTk)
        self.create_grid()
        
    def create_grid(self):
        """ Met a jour l'affichage.. """
        h = self.hauteur
        l = self.largeur
        n = self.n
        m = n-1
        
        out_l =  l//n - 10
        out_h =  h - h//n + 10
        step_h = h//n
        step_l = l//n
            
            
        label = tkinter.Label( text="0")
        label.place(x=out_l, y=out_h)
        
        self.canvas.create_line(l - m*step_l, step_h, l - m*step_l, m*step_h, width=3)
        self.canvas.create_line(l - m*step_l, m*step_h, l - step_l, m*step_h, width=3)
        
        for i in range(m-1) : 
            i = i+1
            self.canvas.create_line(l - i*step_l, step_h, l - i*step_l, m*step_h, width=1)
            self.canvas.create_line(l - m*step_l, i*step_h, l - step_l, i*step_h, width=1)
            
            val = 255-((i-1)*255//(m-1))
            
            label = tkinter.Label( text=str(val))
            label.place(x=l - (i*step_l+10), y=out_h)
            
            label = tkinter.Label( text=str(val))
            label.place(x=out_l-20 , y=(i*step_h))   
        self.canvas.pack()
        

    def callbackHorizontale(self):
        """ Initialise l'outils courant pour ajouter d'une nouvelle horizontale. """
        self.outilsCourant = self.controleur.nouvelleHorizontale()    

    def callbackApprox(self):
        """ Initialise l'outils courant pour ajouter d'une nouvelle horizontale. """
        self.outilsCourant = self.controleur.nouvelleApprox(self.num_click)
        
    def callbackApprox_save(self):
        """ Initialise l'outils courant pour ajouter d'une nouvelle horizontale. """
        #self.outilsCourant = self.controleur.saveApprox() 
        num_points = len(self.all_points)
        max_full = num_points-(num_points%self.num_click)
        selection = self.all_points[max_full-self.num_click:max_full]
        out_str = []
        str_title = ""
        str_x = ""
        str_y = ""
        n = self.n
        for x, y in selection:
            x= (x- self.largeur//n)/((n-1)*self.largeur//n - self.largeur//n )
            y = abs((n-1)*self.hauteur//n -y)/((n-1)*self.hauteur//n - self.hauteur//n )
            str_title += 'val;'
            str_x += str(x) + ';'
            str_y += str(y) + ';'
        out_str.append(str_title[:-1])
        out_str.append(str_x[:-1])
        out_str.append(str_y[:-1])
        if self.dark : 
            file_ = 'functions/function_dark.csv'
        else : 
            file_ = 'functions/function.csv'
        with open(file_, 'w') as outfile:
            outfile.write('\n'.join(str(i) for i in out_str))   
        

    
    def executer(self):
    
        def getBool(event) :
            if self.dark : 
                self.dark = False
            else : 
                self.dark = True
                
        def num_click_selected(event):
            selected_indices = listbox.curselection()
            selected_num = ",".join([listbox.get(i) for i in selected_indices])
            self.num_click = int(selected_num)
            self.callbackNouveau()
            
    
                
        """ Initialise et lance le programme. """
        # fenetre principale
        fenetre = tkinter.Tk()
        fenetre.title("Definir étalonage")
        fenetre.resizable(0, 0)
        # menu
        menu = tkinter.Menu(fenetre)
        fenetre.config(menu=menu)
        filemenu = tkinter.Menu(menu)
        menu.add_cascade(label="Fichier", menu=filemenu)
        filemenu.add_command(label="Nouveau", command=self.callbackNouveau)
        filemenu.add_separator()
        filemenu.add_command(label="Quitter", command=fenetre.destroy)
        toolsmenu = tkinter.Menu(menu)
        menu.add_cascade(label="Outils", menu=toolsmenu)
        toolsmenu.add_command(label="trouver approximation", command=self.callbackApprox)
        toolsmenu.add_command(label="sauvegarder derniere approximation", command=self.callbackApprox_save)

        # Canvas : widget pour le dessin dans la fenetre principale
        self.canvas = tkinter.Canvas(fenetre, width=self.largeur, height=self.hauteur, bg='white')
        self.canvas.bind("<Button-1>", self.callbackButton1)
        self.canvas.bind("<Button-3>", self.callbackButton3)
        
        h = self.hauteur
        l = self.largeur
        self.canvas.create_line(h - h//4, l//4, h - h//4, 3*l//4, width=4)
        self.canvas.pack()
        
        cb = tkinter.Checkbutton(fenetre, text = "Dark images ?", variable = self.dark)
        cb.bind("<Button-1>", getBool)
        cb.pack()
        
        num_click_poss = ('2', '3', '4', '5', '6', '7', '8', '9')
        var = tkinter.Variable(value=num_click_poss)
        listbox = tkinter.Listbox(fenetre, listvariable=var, height=1, selectmode=tkinter.EXTENDED)
        listbox.bind('<<ListboxSelect>>', num_click_selected)
        listbox.pack(expand=True, fill=tkinter.BOTH)
        
        scrollbar = tkinter.Scrollbar(fenetre, orient=tkinter.HORIZONTAL, command=listbox.yview)
        listbox['yscrollcommand'] = scrollbar.set
        scrollbar.pack(side=tkinter.LEFT, expand=True, fill=tkinter.Y)

        # Image : structure contenant les donnees de l'image manipule
        self.image = Image.new("RGB", (self.largeur, self.hauteur), 'lightgrey')
        # ImageDraw : structure pour manipuler l'image
        self.imageDraw = ImageDraw.Draw(self.image)
        # met a jour l'affichage
        self.majAffichage()
        # lance le programme
        fenetre.mainloop()
