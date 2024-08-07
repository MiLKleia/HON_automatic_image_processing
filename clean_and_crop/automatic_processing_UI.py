import numpy as np
import imutils as imutils
import os
import tkinter 
import tkinter.filedialog as filedialog

import functions.FFT_functions as FFT
import functions.yolo_crop as yolo
import functions.sobel_crop as sobel_crop
import functions.clean as clean
import functions.seperate_and_compress as final_steps
import functions.FFT_extract as extract
import functions.FFT_line_erase as line_erase

import UI.Vue as Vue
    
ERROR_NO_FILE = 1
ERROR_NO_REDO = 2
ALL_IMAGES = 'images'


class Folder_Processing(object):
    def __init__(self):
        self.NAME_FOLDER = ""
        self.FOLDER_OG_IMG_REDUCE_SIZE = ""
        self.FOLDER_CLEAN_IMG = ""
        self.FOLDER_CROPPED_ML_IMG = ""
        self.FOLDER_CROP_ERROR_REDO = ""
        self.FOLDER_CROP_CHECK = ""
        self.FOLDER_COMPRESS = ""
        self.FOLDER_LINE_EXTRACT = ""
        self.FOLDER_BORDER_EXTRACT = ""
        self.ratio = 1
        self.ratio_bool = True

        self.MODEL_CNN_CROP ='functions' + os.sep + 'models' + os.sep + '640_s_40' + os.sep + 'best.pt'
        self.spe = False
        
    def display_error(self, val_error):
        root = tkinter.Tk()
        root.title('ERROR')
        root.geometry("250x170")
        if val_error == ERROR_NO_FILE :
            error_msg = "pas de fichier spécifié. \n"
        elif val_error == ERROR_NO_REDO :
            error_msg = "pas de résultat de crop par YOLO \n"
        else :
            error_msg = "erreur inconnue \n"
        T = tkinter.Label(root)
        b2 = tkinter.Button(root, text = "Exit", command = root.destroy) 
        T.pack()
        T.config(text = error_msg)
        b2.pack()
        tkinter.mainloop()
        
    def majAffichage(self):
        self.update_folders_path()
        
    
        
    def update_folders_path(self):
        self.FOLDER_CLEAN_IMG = ALL_IMAGES + os.sep + 'Krita_clean' + os.sep + self.NAME_FOLDER
        self.FOLDER_CROPPED_ML_IMG =  ALL_IMAGES + os.sep + 'ML_cropped' + os.sep + self.NAME_FOLDER
        self.FOLDER_CROP_ERROR_REDO = ALL_IMAGES + os.sep + 'ML_cropped' + os.sep + 'not_cropped'
        self.FOLDER_CROP_CHECK = ALL_IMAGES + os.sep + 'ML_cropped' + os.sep + 'check'
        self.FOLDER_COMPRESS = ALL_IMAGES + os.sep + 'compress' + os.sep + self.NAME_FOLDER
        self.FOLDER_LINE_EXTRACT = ALL_IMAGES + os.sep + 'Krita_no_line' + os.sep + self.NAME_FOLDER
        self.FOLDER_BORDER_EXTRACT = ALL_IMAGES + os.sep + 'extract_contours' + os.sep + self.NAME_FOLDER
              
    def choose_YOLO_model(self):
        file_name = filedialog.askopenfilenames()
        self.path_to_ref = file_name[0]  

    def choose_folder_base_reduce(self):
        file_name = filedialog.askdirectory()
        self.FOLDER_OG_IMG_REDUCE_SIZE = file_name
        self.NAME_FOLDER = os.path.basename(os.path.normpath(file_name))
        self.update_folders_path()

    def getBool_function(self, event) :
        if self.spe : 
            self.spe = False
        else :
            self.spe = True  

    def getBool_ratio(self, event) :
        if self.ratio_bool : 
            self.ratio_bool = False
            self.ratio = 1
        else :
            self.ratio_bool = True 
            self.ratio = 0.5
            
                        
    def clean_and_crop(self):
        if len(self.NAME_FOLDER) == 0:
            self.display_error(ERROR_NO_FILE)
    
        else : 
            clean.folder_krita_clean_line_keep(in_path = self.FOLDER_OG_IMG_REDUCE_SIZE, 
                                            out_path = self.FOLDER_CLEAN_IMG, noisy=self.spe)
            yolo.YOLO_crop_folder(self.FOLDER_CLEAN_IMG, self.FOLDER_CROPPED_ML_IMG, 
                                self.FOLDER_CROP_ERROR_REDO, self.FOLDER_CROP_CHECK, self.MODEL_CNN_CROP, 15)
           
            root = tkinter.Tk()
            root.title('PROCESSING')
            root.geometry("250x170")
            T = tkinter.Text(root, height = 5, width = 52)
            msg = """clean and crop done !"""
            T.pack()
            T.insert(tkinter.END,msg)
            tkinter.mainloop()  
    
    #doesn't work
    def set_functions(self):
        vue = Vue.EtalFunction(800, 600)  
        vue.executer()

    def fill_redo_folder(self):
        if len(self.NAME_FOLDER) == 0:
            self.display_error(ERROR_NO_FILE)
        elif not os.path.isdir(self.FOLDER_CROP_CHECK) :
            self.display_error(ERROR_NO_REDO)
    
        else : 
            final_steps.fill_redo_folder(self.FOLDER_CROP_CHECK, self.FOLDER_CROP_ERROR_REDO, self.FOLDER_OG_IMG_REDUCE_SIZE)
        
            root = tkinter.Tk()
            root.title('PROCESSING')
            root.geometry("250x170")
            T = tkinter.Text(root, height = 5, width = 52)
            msg = """redo folder filled"""
            T.pack()
            T.insert(tkinter.END,msg)
            tkinter.mainloop()     
        
        
    def compress(self):
        if len(self.NAME_FOLDER) == 0:
            self.display_error(ERROR_NO_FILE)
        elif not os.path.isdir(self.FOLDER_CROPPED_ML_IMG) :
            self.FOLDER_CROPPED_ML_IMG = self.FOLDER_OG_IMG_REDUCE_SIZE
        else : 
            final_steps.compress_jpg(self.FOLDER_CROPPED_ML_IMG, self.FOLDER_COMPRESS)
        
            root = tkinter.Tk()
            root.title('PROCESSING')
            root.geometry("250x170")
            T = tkinter.Text(root, height = 5, width = 52)
            msg = """compression done"""
            T.pack()
            T.insert(tkinter.END,msg)
            tkinter.mainloop()     
        
    def remove_grid(self):
        if len(self.NAME_FOLDER) == 0:
            self.display_error(1)
        
        else : 
            line_erase.line_erase_files_in_folder(self.FOLDER_OG_IMG_REDUCE_SIZE, self.FOLDER_LINE_EXTRACT, self.ratio)
        
            root = tkinter.Tk()
            root.title('PROCESSING')
            root.geometry("250x170")
            T = tkinter.Text(root, height = 5, width = 52)
            msg = """lines erased"""
            T.pack()
            T.insert(tkinter.END,msg)
            tkinter.mainloop() 
        
    def extract_contour(self):
        if len(self.NAME_FOLDER) == 0:
            self.display_error(ERROR_NO_FILE)
    
        else : 
            extract.extract_border_files_in_folder(self.FOLDER_OG_IMG_REDUCE_SIZE, self.FOLDER_BORDER_EXTRACT, self.ratio, KEEP_LINE = False)
        
            root = tkinter.Tk()
            root.title('PROCESSING')
            root.geometry("250x170")
            T = tkinter.Text(root, height = 5, width = 52)
            msg = """contours extracted"""
            T.pack()
            T.insert(tkinter.END,msg)
            tkinter.mainloop() 
        
        
    def executer(self):
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
        imagesmenu.add_command(label="Choisir le dossier d'images originales", command=self.choose_folder_base_reduce)
        imagesmenu.add_command(label="Choisr le modèle YOLO", command=self.choose_YOLO_model)


        button1=tkinter.Button(fenetre, text="choisir dossier",command=self.choose_folder_base_reduce, width=20, height = 1)
        button1.grid(row=1,column=0)
        
        button2=tkinter.Button(fenetre, text="nettoyer et recadrer",command=self.clean_and_crop, width=20, height = 1)
        button2.grid(row=2,column=0)
        button3=tkinter.Button(fenetre, text="remplir dossier à refaire",command=self.fill_redo_folder, width=20, height = 1)
        button3.grid(row=2,column=1)
        button4=tkinter.Button(fenetre, text="compresser",command=self.compress, width=20, height = 1)
        button4.grid(row=2,column=2)
        
        button5=tkinter.Button(fenetre, text="effacer lignes",command=self.remove_grid, width=20, height = 1)
        button5.grid(row=3,column=1)
        button6=tkinter.Button(fenetre, text="extraction contours",command=self.extract_contour, width=20, height = 1)
        button6.grid(row=3,column=2)
        
        cb1 = tkinter.Checkbutton(fenetre, text = "Utiliser les fonctions speciales", variable = self.spe)
        cb1.bind("<Button-1>", self.getBool_function)
        cb1.grid(row=1,column=2)
        
        cb2 = tkinter.Checkbutton(fenetre, text = "Ne pas réduier taille image ?\n(long)", variable = self.ratio_bool)
        cb2.bind("<Button-1>", self.getBool_ratio)
        cb2.grid(row=3,column=0)
        
        
        for i in range(3):
            fenetre.grid_columnconfigure(i+1, minsize=900//3)
            fenetre.grid_rowconfigure(i+1, minsize=13)
        
        
        self.majAffichage()
        # lance le programme
        fenetre.mainloop()
        
        
        
if __name__ == "__main__":
    # cree la vue
    vue = Folder_Processing()   
    # lance le programme 
    vue.executer()
