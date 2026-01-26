# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 13:20:34 2024

@author: Matthias URSET
"""

#Import des modules 
import numpy as np
import os

#on définit une fonction pour enlever les n premiers points de la liste L
def enlever_n_premiers_points (L,n) :
    Ls=[]
    for i in range((len(L)-n)):
        Ls.append(L[i+n])
    return (Ls)

#On définit une fonction pour enlever les n derniers points de la liste L
def enlever_n_derniers_points (L,n) :
    Ls=[]
    for i in range((len(L)-n)):
        Ls.append(L[i])
    return (Ls)

#On définit une fonction pour supprimer les points au-delà d'une valeur n dans la liste des abscices
def enlever_les_points_sup_à_n (X,Y,n):
    i=0
    while i<len(X):
        if X[i]>n:
            X.remove(X[i])
            Y.remove(Y[i])
        else :
            i+=1
    return(X,Y)

#On définit une fonction pour supprimer les points inférieure à une valeur n dans la liste des abscices
def enlever_les_points_inf_à_n (X,Y,n):
    i=0
    while i<len(X):
        if X[i]<n:
            X.remove(X[i])
            Y.remove(Y[i])
        else :
            i+=1
    return(X,Y)

#On définit une fonction pour convertir une liste à l'échelle logarithmique.
def échelle_log(L):
    ListLlog = []
    for i in range (len(L)):
        ListLlog.append(np.log10(L[i]))
    return(ListLlog)
        
#On définit une fonction pour faire une moyenne glissante (sur M points, M impair) sur la liste des ordonées, à partir d'un certain point (N) dans la liste des absices.
def moyenne_glissante (X,Y,M,N):
    Y_lissé=[]
    m=int((M-1)/2)
    for i in range (len(X)-m):
        if X[i]<N :
            Y_lissé.append(Y[i])
        else :
            yk=0
            for k in range(M):
                yk=yk+Y[(i-m+k)]
            Y_lissé.append((yk/M))
    X=enlever_n_derniers_points(X, m)
    return(X,Y_lissé)

#Réarange une matrice de vecteurs en une matrice
def concat(M):
    M0=[]
    for i in range(len(M)):
        M0.append(M[i])
    return (M0)

#sauvegarde un fichier texte à l'endroit souhaité
def save(I):
    Path=input("entrer le chemin du dossier : ")
    Folder_name=input("entrer le nom du dossier : ")
    File_name="Intrégale.txt"
    new_folder_path = Path+'\\'+Folder_name #Emplacement du dossier où seront enregistrées les courbes
    os.makedirs(new_folder_path, exist_ok=True) # Création du dossier
    File_path=os.path.join(new_folder_path,File_name)
    with open(File_path, 'w') as file:
        file.write(str(I*10**6)+' uJ')

#Pour une liste L multipli chaque élément par N
def scale(L,N):
    for i in range(len(L)):
        L[i]=L[i]*N
    return(L)

#Tronque une liste entre les indices a et b
#def tron_ind(L, a, b):

#Les les vecteurs (X et Y) d'une matrice [X,Y] aux points d’abscisse appartenant à (xa,xb)
#def tron_abs(M, xa, xb):