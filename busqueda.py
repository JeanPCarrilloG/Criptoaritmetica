import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
import statsmodels.api as sm
from statsmodels.formula.api import ols
from types import MethodType
from random import choice
from time import time


class Nodo:

    # Clase para crear los nodos

    def __init__(self, estado, madre, accion, costo_camino, codigo):
        self.estado = estado
        self.madre = madre
        self.accion = accion
        self.costo_camino = costo_camino
        self.codigo = codigo

def nodo_hijo(problema, madre, accion):
    
    # Función para crear un nuevo nodo
    # Input: problema, que es un objeto de clase CriptoAritmetica
    #        madre, que es un nodo,
    #        accion, que es una acción que da lugar al estado del nuevo nodo
    # Output: nodo
    
    estado = problema.transicion(madre.estado, accion)
    costo_camino = madre.costo_camino + problema.costo(madre.estado, accion)
    codigo = problema.codigo(estado)
    return Nodo(estado, madre, accion, costo_camino, codigo)

def depth(nodo):
    print(nodo.accion)
    if nodo.madre == None:
        return 0
    else:
        return depth(nodo.madre) + 1
    
def solucion(n):
    if n.madre == None:
        return []
    else:
        return solucion(n.madre) + [n.accion]

def camino_codigos(nodo):
    if nodo.madre == None:
        return [nodo.codigo]
    else:
        return camino_codigos(nodo.madre) + [nodo.codigo]

def is_cycle(nodo):
    codigos = camino_codigos(nodo)
    return len(set(codigos)) != len(codigos)

def expand(problema, nodo):
    s = nodo.estado
    nodos = []
    for accion in problema.acciones_aplicables(s):
        hijo = nodo_hijo(problema, nodo, accion)
        nodos.append(hijo)
    return nodos

def backtracking_search(problema, estado):

    '''Función de búsqueda recursiva de backtracking'''

    if problema.test_objetivo(estado):
            return estado
    acciones = problema.acciones_aplicables(estado)
    for a in acciones:
        hijo = problema.transicion(estado, a)
        resultado = backtracking_search(problema, hijo)
        if resultado is not None:
            return resultado
    return None

class ListaPrioritaria():

    def __init__(self):
        self.diccionario = {}

    def __str__(self):
        cadena = '['
        inicial = True
        for costo in self.diccionario:
            elementos = self.diccionario[costo]
            for elemento in elementos:
                if inicial:
                    cadena += '(' + str(elemento) + ',' + str(costo) + ')'
                    inicial = False
                else:
                    cadena += ', (' + str(elemento) + ',' + str(costo) + ')'

        return cadena + ']'

    def push(self, elemento, costo):
        try:
            self.diccionario[costo].append(elemento)
        except:
            self.diccionario[costo] = [elemento]

    def pop(self):
        min_costo = np.min(np.array(list(self.diccionario.keys())))
        candidatos = self.diccionario[min_costo]
        elemento = candidatos.pop()
        if len(candidatos) == 0:
            del self.diccionario[min_costo]
        return elemento

    def is_empty(self):
        return len(self.diccionario) == 0

def best_first_search(problema, f=None):
    
    '''Función de búsqueda best_first_search'''
    
    if not f == None:
        problema.costo = MethodType(f, problema)
    s = problema.estado_inicial
    cod = problema.codigo(s)
    nodo = Nodo(s, None, None, 0, problema.codigo(s))
    frontera = ListaPrioritaria()
    frontera.push(nodo, 0)
    explorados = {}
    explorados[cod] = 0
    contador = 0
    while not frontera.is_empty():
        contador = contador + 1
        nodo = frontera.pop()
        if problema.test_objetivo(nodo.estado):
            return nodo
        for hijo in expand(problema, nodo):
            s = hijo.estado
            cod = problema.codigo(s)
            c = hijo.costo_camino
            if (cod not in explorados.keys()) or (c < explorados[cod]):
                frontera.push(hijo, c)
                explorados[cod] = c

    return None

### Funciones con alteraciones

def breadth_first_search(problema, estado):
    
    '''Función de búsqueda breadth-first'''
    
    if problema.test_objetivo(estado):
            return estado
    frontera = [estado]
    while len(frontera) > 0:
        estado = frontera.pop(0) 
        acciones = problema.acciones_aplicables(estado)
        for a in acciones:
            hijo = problema.transicion(estado, a)
            #print("hijo",hijo)
            if problema.test_objetivo(hijo):
                return hijo
            frontera.append(hijo)
    return None

### Funciones Comparación empírica de tiempos

def obtiene_tiempos(fun, args, num_it=1):
    tiempos_fun = []
    for i in range(num_it):
        arranca = time()
        x = fun(*args)
        para = time()
        tiempos_fun.append(para - arranca)
    return tiempos_fun

def compara_funciones(funs, arg, nombres, N=2):
    nms = []
    ts = []
    print(funs)
    for i, fun in enumerate(funs):
        nms += [nombres[i] for x in range(N)]
        breadth_first_search
        ts += obtiene_tiempos(fun, [arg], N)
    data = pd.DataFrame({'Función':nms, 'Tiempo':ts})
    # Graficando
    fig, ax = plt.subplots(1,1, figsize=(3*len(funs),3), tight_layout=True)
    sns.boxplot(data=data, x='Función', y='Tiempo')
    sns.swarmplot(data=data, x='Función', y='Tiempo', color='black', alpha = 0.5, ax=ax);
    # Anova diferencia de medias
    model = ols('Tiempo ~ C(Función)', data=data).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    print(anova_table)

### Anexó Funciones

def nuevo_estado(problema, estado):
    '''
    Función nuevo estado con selección aleatoria
    Entradas:
        estado: Estado inicial
    Salidas:
        estado_asignado: Estado inicial con una nueva opción aleatoria asignada
    '''
    acciones = problema.acciones_aplicables(estado)
    accion = choice(acciones)
    estado_asignado = problema.transicion(estado, accion)
    return (estado_asignado)

def backtracking_search_aleatory_state(problema, estado):
    '''
    Función con implementación de la función de búsqueda recursiva de backtracking
    con asignación de entradas aleatorias
    '''
    condicion = 1
    while condicion != 0 :
        
        estado_aleatorio = estado
        
        for iteracion in range(0,len(estado)-2):
            estado_aleatorio = nuevo_estado(problema, estado_aleatorio)

        busqueda = breadth_first_search(problema, estado_aleatorio)

        if busqueda is not None:
            condicion = 0
            return busqueda
        else:
            condicion = 1
    return

def breadth_first_aleatory_state(problema, estado):
    '''
    Función con implementación de la función de búsqueda breadth-first
    con asignación de entradas aleatorias
    '''
    condicion = 1
    while condicion != 0 :

        estado_aleatorio = estado
        
        for iteracion in range(0,len(estado)-2):
            estado_aleatorio = nuevo_estado(problema, estado_aleatorio)

        busqueda = breadth_first_search(problema, estado_aleatorio)

        if busqueda is not None:
            condicion = 0
            return busqueda
            
        else:
            condicion = 1
    return

def best_first_search_response_effective(problema, estado):
    '''
    Función con implementación de la función de búsqueda best_first_search
    con asignación de entradas aleatorias
    '''
    busqueda = best_first_search(problema)
    
    condicion = 1
    while condicion != 0:
        
        if busqueda is not None:
            camino = solucion(busqueda)
            condicion = 0
            return camino
        else:
            condicion = 1
    return
