import copy
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import AnnotationBbox, OffsetImage, TextArea
from time import sleep
from IPython.display import clear_output
import numpy as np
import pandas as pd
import random as rd
from PIL import Image, ImageDraw, ImageFont
import networkx as nx
from itertools import product, permutations
from nltk import Tree

class CriptoAritmetica():

    def __init__(self, lista_palabras):
        self.palabras = lista_palabras
        self.lista_letras = [letra for palabra in self.palabras for letra in palabra ]
        self.lista_letras = list(set(self.lista_letras))
        self.estado_inicial = {letra:None for letra in self.lista_letras}
        self.letras_iniciales = list(set(palabra[0] for palabra in self.palabras))
        
    def pintar_estado(self, estado):
        # Dibuja el problema inicial, el estado del que se habla (ya sea la solución o no) y devuelve el resultado de la operación.
        # Input: Estado - diccionario con el estado de las letras del problema.
        fig, axes = plt.subplots(figsize=(5,len(self.palabras)))
        white = np.ones((100, 100), dtype=np.float)
        list_len = [len(palabra) for palabra in self.palabras]

        plt.text(0.2, 1.5, 'Problema inicial', fontsize = 20, color = 'blue')
        plt.text(1.5, 1.5, 'Estado', fontsize = 20, color = 'blue')
        plt.text(2.5, 1.5, 'Resultado', fontsize = 20, color = 'blue')
        plt.text(0, 1.3, '----------------------------------------------------------------------------------------------------------------------------', fontsize = 20, color = 'blue')

        for i in range(len(self.palabras)):
            if i == len(self.palabras) - 2:
                plt.text(0.2, (len(self.palabras)-i)/len(self.palabras), f"+      {self.palabras[i]}", fontsize = 20)
                plt.text(0.2, 3/2*1/len(self.palabras), '----------------', fontsize = 20)
            else:
                plt.text(0.4, (len(self.palabras)-i)/len(self.palabras), self.palabras[i], fontsize = 20)

        q = 0
        for est in estado:
            plt.text(1.4, (len(estado)-q)/len(estado), '|', fontsize = 20, color = 'blue')
            plt.text(1.5, (len(estado)-q)/len(estado), est, fontsize = 20)
            plt.text(1.6, (len(estado)-q)/len(estado), '|', fontsize = 20, color = 'blue')
            plt.text(1.8, (len(estado)-q)/len(estado), '|', fontsize = 20, color = 'blue')
            if estado[est] == None:
                plt.text(1.7, (len(estado)-q)/len(estado), '-', fontsize = 20)
            else:
                plt.text(1.7, (len(estado)-q)/len(estado), str(estado[est]), fontsize = 20)
            q += 1

        if self.test_objetivo(estado):
            for i in range(len(self.palabras_sol)):
                if i == len(self.palabras_sol) - 2:
                    plt.text(2.5, (len(self.palabras_sol)-i)/len(self.palabras_sol), f"+      {self.palabras_sol[i]}", fontsize = 20)
                    plt.text(2.5, 3/2*1/len(self.palabras_sol), '----------------', fontsize = 20)
                else:
                    plt.text(2.7, (len(self.palabras_sol)-i)/len(self.palabras_sol), str(self.palabras_sol[i]), fontsize = 20)
        else:
            plt.text(2.5, 1, "El estado no es", fontsize = 20)
            plt.text(2.3, 0.7, "una solución al problema.", fontsize = 20)

        axes.axis('off')

        return

    def transicion(self, estado, accion):
        # Dada una acción se cambia el estado del problema.
        # Input: acción - Dupla con la letra y el valor que se desea cambiar en el diccionario.
        # Output: Estado que es un diccionario.
        estado_copy = copy.deepcopy(estado)
        estado_copy[accion[0]] = accion[1]
        return estado_copy

    def acciones_aplicables(self, estado):
        # Devuelve una lista de tuplas que representan
        # la acción permitida, de acuerdo a la codificación
        # presentada en al formalización del problema más arriba.
        # Input: Estado - diccionario con el estado de las letras del problema.
        # Output: acciones - Lista de tuplas.
        digitos_disponibles = [d for d in range(10) if d not in estado.values()]
        letras_disponibles = [d for d in self.lista_letras if estado[d] == None]
        acciones = list(product(letras_disponibles, digitos_disponibles))
        for letra in self.letras_iniciales:
            try:
                if (letra, 0) in acciones:
                    acciones.remove((letra, 0))
            except ValueError:
                    acciones.remove((letra))
        return acciones
    
    def test_objetivo(self, estado):
        # Devuelve True/False dependiendo si el estado
        # resuelve el problema
        # Input: estado - diccionario de las letras con sus respectivos valores.
        # Output: True/False
        self.palabras_sol = []
        for palabra in self.palabras:
            for letra in palabra:
                palabra = palabra.replace(letra, str(estado[letra]))
            try:
                num_palabra = int(palabra)
                self.palabras_sol.append(num_palabra)
            except:
                return False
        return np.sum(self.palabras_sol[:-1]) == self.palabras_sol[-1]

    def codigo(self, estado):
        str_codigo = ""
        for i in estado:
            if estado[i] != None:
                str_codigo += f"{i}-{estado[i]} "
        return str_codigo

    def costo(self, estado, accion):
        return 0
