"""
@author: Matthias URSET

Useful functions draw and save graphs
"""
#Import des modules 
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.widgets import Cursor

#Enregistre les graphs superposés des paires de vecteurs contenues dans, aux formats .png et .pdf 
def graphsup(M,Path,Repo,Fig_name,Y_Axes,X_Axe):
    new_folder_path = Path+'\\'+Repo#Emplacement du dossier où seront enregistrées les courbes
    os.makedirs(new_folder_path, exist_ok=True) # Création du dossier
    fig, ax = plt.subplots( nrows=1, ncols=1 )  # Définition de la figure
    ax.set_title(Fig_name)
    ax.set_xlabel(X_Axe)
    for i in range (len(M)) :
        label=str(Y_Axes[i])
        ax.plot(M[i][0],M[i][1],label=label)
    ax.legend()
    fig.savefig(Path+'\\'+Repo+'\\'+Fig_name+'.png')   # Enregistrement de la figure au format .png
    fig.savefig(Path+'\\'+Repo+'\\'+Fig_name+'.pdf')   # Enregistrement de la figure au format .pdf
    plt.close(fig)

#Enregistre les graphs séparés des paires de vecteurs contenues dans, aux formats .png et .pdf 
#Fig_name,Y_Axe,X_Axe sont des listes de longueur len(M)
def multigraph(M,Path,Repo,Fig_name,Y_Axe,X_Axe, Y_min: float | None = None , Y_max: float | None = None, X_min: float | None = None , X_max: float | None = None):
    new_folder_path = Path+'\\'+Repo#Emplacement du dossier où seront enregistrées les courbes
    os.makedirs(new_folder_path, exist_ok=True) # Création du dossier
    for i in range (len(M)) :
        fig, ax = plt.subplots( nrows=1, ncols=1 )  # Définition de la figure
        ax.plot(M[i][0],M[i][1])
        ax.set_title(str(Fig_name[i]))
        ax.set_xlabel(str(X_Axe[i]))
        ax.set_ylabel(str(Y_Axe[i]))
        if Y_min is not None and Y_max is not None :
            ax.set_ylim(Y_min,Y_max)
        if X_min is not None and X_max is not None :
            ax.set_xlim(X_min,X_max)      
        fig.savefig(Path+'\\'+Repo+'\\'+str(Fig_name[i])+'.png')   # Enregistrement de la figure au format .png
        fig.savefig(Path+'\\'+Repo+'\\'+str(Fig_name[i])+'.pdf')   # Enregistrement de la figure au format .pdf
        plt.close(fig)