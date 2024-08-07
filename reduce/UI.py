import numpy as np
import imutils as imutils
import os
import tkinter 
import tkinter.filedialog as filedialog

from ima_mod import from_tiff, resize_folder

    
ERROR_NO_FILE = 1
INVALID_RATIO = 2
ALL_IMAGES = 'images'

GLOBAL_RATIO = 0.2
def modify_GLOBAL_RATIO(n):
    global GLOBAL_RATIO 
    try:
        val = float(n)
        if val > 0. and val < 1.5 :
            GLOBAL_RATIO = val
        else : 
            print('entry must be less than 1.5 and more than 0')
    except ValueError:
        print('invalide type. entry must be float')


class Folder_Processing(object):
    
    
    def __init__(self):
        self.FOLDER_TIFF = "tiff"
        self.FOLDER_NEW_TYPE = "type_change"
        self.FOLDER_RESIZE = "resize"
        self.FOLDER_REDUCE = "reduce"
        self.NAME_FOLDER = ""
        self.type  = 'jpg'
        self.reduce_bool = False
        self.bool_JPG = True
        
    def display_error(self, val_error):
        root = tkinter.Tk()
        root.title('ERROR')
        root.geometry("250x170")
        if val_error == ERROR_NO_FILE :
            error_msg = "pas de dossier choisi \n"
        elif val_error == INVALID_RATIO :
            error_msg = "valeur invalide \n"
        else :
            error_msg = "erreur inconnue \n"
        T = tkinter.Label(root)
        b2 = tkinter.Button(root, text = "Exit", command = root.destroy) 
        T.pack()
        T.config(text = error_msg)
        b2.pack()
        #tkinter.mainloop()
        
        

    def choose_folder(self):
        file_name = filedialog.askdirectory()
        self.FOLDER_TIFF = file_name
        self.NAME_FOLDER = os.path.basename(os.path.normpath(file_name))

    def getBool_reduce(self, event) :
        if self.reduce_bool : 
            self.reduce_bool = False
        else :
            self.reduce_bool = True 

    def getBool_type(self, event) :
        if self.bool_JPG : 
            self.bool_JPG = False
            self.type  = 'png'
        else :
            self.bool_JPG = True 
            self.type  = 'jpg' 

            

    def ask_ratio(self):
        def get_entry_value():
            n = entry.get()
            modify_GLOBAL_RATIO(n)
            root.destroy()
            
        root = tkinter.Tk()
        root.title("choix du ratio")
        entry = tkinter.Entry(root)
        entry.pack()
        button = tkinter.Button(root, text="sélectionner", command=get_entry_value)
        button.pack()

        
        
    
    def tiff_to_other(self):
        if len(self.FOLDER_TIFF) == 0:
            self.display_error(ERROR_NO_FILE)
    
        else : 
            from_tiff(self.FOLDER_TIFF, self.FOLDER_NEW_TYPE, self.type)
        
            root = tkinter.Tk()
            root.title('PROCESSING')
            root.geometry("250x170")
            T = tkinter.Label(root)
            msg = """.tiff traitées \n"""
            T.pack()
            T.config(text = msg)
            #tkinter.mainloop() 
            
            
    def reduce_and_resize(self):
        if len(self.FOLDER_TIFF) == 0:
            self.display_error(ERROR_NO_FILE)
    
        else : 
            resize_folder(self.FOLDER_NEW_TYPE, self.FOLDER_RESIZE, self.FOLDER_REDUCE, GLOBAL_RATIO, self.reduce_bool)
        
            root = tkinter.Tk()
            root.title('PROCESSING')
            root.geometry("250x170")
            T = tkinter.Label(root)
            msg = """reduction de taille terminée \n"""
            if self.reduce_bool : 
                msg = """reduction de taille et \n de poids terminées \n"""
            T.pack()
            T.config(text = msg)
            #tkinter.mainloop() 
               
    
    def executer(self):
    
        def majAffichage():
            label_ratio.config(text = "ratio : " + str(GLOBAL_RATIO))
            fenetre.after(500, majAffichage)
            
            
        """ Initialise et lance le programme. """
        # fenetre principale
        fenetre = tkinter.Tk()
        fenetre.title("Processing")
        fenetre.geometry("800x150")
        fenetre.resizable(0, 0)
        # menu
        menu = tkinter.Menu(fenetre)
        fenetre.config(menu=menu)
        filemenu = tkinter.Menu(menu)
        menu.add_cascade(label="Fichier", menu=filemenu)
        filemenu.add_separator()
        filemenu.add_command(label="Quitter", command=fenetre.destroy)
        imagesmenu = tkinter.Menu(menu)
        menu.add_cascade(label="Chemins", menu=imagesmenu)
        imagesmenu.add_command(label="Choisir le dossier d'images", command=self.choose_folder)


        button1=tkinter.Button(fenetre, text="choisir dossier",command=self.choose_folder, width=20, height = 1)
        button1.grid(row=1,column=0)
        
        button2=tkinter.Button(fenetre, text="PNG/JPG",command=self.tiff_to_other, width=20, height = 1)
        button2.grid(row=1,column=1)
        button3=tkinter.Button(fenetre, text="RESIZE",command=self.reduce_and_resize, width=20, height = 1)
        button3.grid(row=1,column=2)
        
        button6=tkinter.Button(fenetre, text="choisir ratio",command=self.ask_ratio, width=20, height = 1)
        button6.grid(row=2,column=1)
        
        label_ratio = tkinter.Label(fenetre)
        label_ratio.grid(row=2,column=0)
        label_ratio.config(text = "ratio : " + str(GLOBAL_RATIO))
        
        cb1 = tkinter.Checkbutton(fenetre, text = "reduire poids ?", variable = self.reduce_bool)
        cb1.bind("<Button-1>", self.getBool_reduce)
        cb1.grid(row=2,column=2)
        
        cb2 = tkinter.Checkbutton(fenetre, text = "PNG ?", variable = self.bool_JPG)
        cb2.bind("<Button-1>", self.getBool_type)
        cb2.grid(row=3,column=1)
        
        for i in range(3):
            fenetre.grid_columnconfigure(i+1, minsize=900//3)
            fenetre.grid_rowconfigure(i+1, minsize=13)
        
        
        majAffichage()
        
        # lance le programme
        fenetre.mainloop()
        
        
        
if __name__ == "__main__":
    # cree la vue
    vue = Folder_Processing()   
    # lance le programme 
    vue.executer()
