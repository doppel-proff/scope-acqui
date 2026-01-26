"""
Created on Mon Oct 14 13:20:34 2024

@author: Matthias URSET
"""

#Import des modules 

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import argrelextrema

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

#En entrée 4 listes, ordonnées et abscises, de deux fonctions sinusoïdales.
#Calcul selon la méthode des moindres carrés les fonctions A*sin(2*pi*f+phi) les plus proches
#Retourne la différence de phase entre ces fonctions  
def phase(Ya,Xa,Yb,Xb):
    def sinusoidal(t, A, f, phi):
        return A * np.sin(2 * np.pi * f * t + phi)
    params_a, _ = curve_fit(sinusoidal, Xa, Ya, p0=[0.3, 1000.0, 0.0])
    params_b, _ = curve_fit(sinusoidal, Xb, Yb, p0=[1.0, 1000.0, 0.0])
    A_est_a, f_est_a, phi_est_a = params_a
    A_est_b, f_est_b, phi_est_b = params_b
    delta_phi = phi_est_b - phi_est_a
    return (delta_phi)

#En entrée 4 listes, ordonnées et abscises, de deux fonctions sinusoïdales.
#Calcul selon la méthode des moindres carrés les fonctions A*sin(2*pi*f+phi) les plus proches
#Retourne le rapport d'amplitudes entre ces fonctions  
def module(Ya,Xa,Yb,Xb):
    def sinusoidal(t, A, f, phi):
        return A * np.sin(2 * np.pi * f * t + phi)
    params_a, _ = curve_fit(sinusoidal, Xa, Ya, p0=[0.3, 1000.0, 0.0])
    params_b, _ = curve_fit(sinusoidal, Xb, Yb, p0=[1.0, 1000.0, 0.0])
    A_est_a, f_est_a, phi_est_a = params_a
    A_est_b, f_est_b, phi_est_b = params_b
    M = A_est_a / A_est_b
    return (M)

#Pour une liste abscises, ordonnées, retourne la matrice (X[i],Y[i]), des N maximums locaux 
def recherche_n_maximums(x_values, y_values, N):
    x_values = np.array(x_values)
    y_values = np.array(y_values)

    # Trouver les indices des maximums locaux
    max_indices = argrelextrema(y_values, np.greater)[0]

    # Extraire les coordonnées des maximums locaux
    max_points = [(x_values[i], y_values[i]) for i in max_indices]

    # Trier les maximums par valeur décroissante
    max_points_sorted_by_value = sorted(max_points, key=lambda point: point[1], reverse=True)

    # Filtrer les maximums trop proches
    filtered_points = []
    min_distance = 0.01 * np.max(x_values)
    for pt in max_points_sorted_by_value:
        if all(abs(pt[0] - fp[0]) > min_distance for fp in filtered_points):
            filtered_points.append(pt)
        if len(filtered_points) == N:
            break

    # Trier les N plus grands par x croissant
    top_n_sorted_by_x = sorted(filtered_points, key=lambda point: point[0])

    # Séparer les abscisses et ordonnées
    abscisses = [pt[0] for pt in top_n_sorted_by_x]
    ordonnees = [pt[1] for pt in top_n_sorted_by_x]

    return (abscisses, ordonnees)
