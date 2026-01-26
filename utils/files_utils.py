"""
Created on Mon Oct 14 13:20:34 2024

@author: Matthias URSET
"""

#Import des modules 
import numpy as np
import os
import shutil

#retourne sous forme de matrice les valeurs contenues dans un fichier .csv
def open_csv(File):
    Dcsv = open(str(File))# Dcsv variable pour la liste csv.
    D = np.genfromtxt(Dcsv, delimiter=",")# D Liste du document csv au format np.array
    return (D)

#sauvegarde une valeur dans un fichier texte à l'endroit souhaité
def save_value(Value, Path, Folder_name, File_name, Unit):
    File_name= File_name+".txt"
    new_folder_path = Path+'\\'+Folder_name #Emplacement du dossier où seront enregistrées les courbes
    os.makedirs(new_folder_path, exist_ok=True) # Création du dossier
    File_path=os.path.join(new_folder_path,File_name)
    with open(File_path, 'w') as file:
        file.write(str(Value)+ Unit)

#Parcour les fichiers d'un répertoire et retourne la liste des noms de chaque fichier 
def parcour(Dir):
    L=[]
    for N in os.listdir(Dir):
        Path = os.path.join(Dir,N)
        if os.path.isfile(Path):
            L.append(N)
    return L

#Dans un str supprime le point et les caractères suivants
def del_ext(File) -> str:
    return File.split('.')[0]

def return_ext (File) :
    return File.split('.')[1]

def sort_ext(Dir):
    L = parcour(Dir) 
    for File in L:
        Path = os.path.join(Dir,File)
        Ext = return_ext(File)
        New_Dir = os.path.join(Dir,Ext)
        os.makedirs(New_Dir, exist_ok=True)
        File_Path = os.path.join(New_Dir,File)
        shutil.move (Path,File_Path)
        #print("Files sorted according to their extention")

# Enregistre un tuple au format csv
def save_tuple_csv(Lx,Ly,Path,Repo,File_name):
    os.makedirs(os.path.join(Path,Repo), exist_ok = True)
    File_Path = os.path.join(Path,Repo,File_name)
    Data = np.column_stack((Lx,Ly))
    np.savetxt(File_Path, Data, delimiter=";", fmt="%9f") #enrgistrés avec 6 decimals après la virgule

#Sauvegarde un vecteur au format csv
#def save_csv_vect(L, Path, Folder_name, File_name):

#Sauvegarde un vecteur dans la colone N d'un fichier excel
#def save_xlsx_vect(L,N, Path, Folder_name, File_name):

#Sauvegarde une matrice au format csv
#def save_csv_vect(M, Path, Folder_name, File_name):

#Sauvegarde une matrice dans un fichier excel
#def save_xlsx_vect(M, Path, Folder_name, File_name):