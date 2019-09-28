'''
-----------------------  E S Q U I V E L --------------------------------
    Titulo, honor a Juan Garcia Esquivel
    Info: Generativa automática de canciones
    Autor: Raúl Antonio Ortega Vallejo
-------------------------------------------------------------------------
    Bibliotecas requeridas por el programa 
-------------------------------------------------------------------------
    Uso de la biblioteca: 'fonetica3':
    Autor: Carlos Daniel Hernandez Mena 
    https:/github.com/CarlosDanielMena/Libreria_Fonetica3
-------------------------------------------------------------------------
'''
from collections import defaultdict # Diccionarios de Listas
from Frase.frase import Frase # Clase Frase
import csv

class Corpus:
    def __init__(self,archivo, mapeo = False#Por default no se hace el mapeo
                  ):
        '''
        Clase Corpus
        Gestiona un corpusc (ya procesado, en CSV) 
        acorde a la estructura propuesta
        '''
        self.corpus = None  # Copus, todas las canciones
        self.mapeo = None # Mapeo de indices / Tabla hash
        self.generos = set()
        ' Inicializamos los contadores '
        self.noCancion = 0 # Identificador de Canción iterada
        self.noLineas = 0  # No. Total de frases / líneas de texto
        self.contador = 0 # Contador de canciones rechazadas por la rutina de mapeo
        self.procesar(archivo, mapeo) #Procesamos el achivo CSV

    def mapearLetra(self,cadena):
        # Contador de canciones
        i = self.noCancion
        # Contador de frases de la canción
        j = 0
        for frase in cadena:
            try:
                nueva = Frase(frase)
                nSilabas = nueva.tamSilabas;
                vocalTonica = nueva.indicesFoneticos[-1]
                self.mapeo[(vocalTonica, nSilabas)].append([i, j])
                # Liberar memoria
                del nueva
            except:
                'Contador de canciones no mapeadas'
                self.contador += 1
                #print("Frase %d rechazada: %s" % (self.contador,frase))
            j += 1

    def procesar(self,archivo,mapeo = False):
        if not self.corpus:
            self.corpus = list()
            self.mapeo = defaultdict(list)
            archivo += ".csv"
            # Inicializamos la tabla hash
            try:
                with open(archivo, newline='') as csvfile:
                    diccionario =  csv.DictReader(csvfile)
                    for fila in diccionario:
                        linea = fila['letra'].split("\n")[:-1]
                        self.noLineas += len(linea)
                        fila['letra'] = linea
                        if mapeo:
                            self.mapearLetra(linea)
                        self.corpus.append(fila)
                        self.noCancion += 1
                        self.generos.add(fila['genero'])
                self.mapeo = dict(self.mapeo)
                ' Debug '
                #print("Frases rechazadas: ",self.contador)
                #print(self.corpus[cancion]['letra'][frase])
            except:
                print ("Error intentar procesar el corpus")

    def destruir(self):
        '''
        Destruye varios atributos de la clase Corpus
        '''
        self.corpus.clear() # Corpus
        self.mapeo.clear()  # Mapa de inidices del corpus

    def imprimirLetra(self,letra):
        for palabra in letra: print(palabra)

    def iterar(self):
        # El separador mejora la visualización de las líneas 
        separador = '>' * 100 
        for dic in self.corpus:
            print("%s %s" % (separador, dic['titulo'].upper()))
            self.imprimirLetra(dic['letra'])
        # Imprimos el total de frases y canciones
        print("%s Líneas de texto: %s  Total de Canciones: %s" % (separador,self.noLineas,self.noCancion))
        print(separador,"Generos:",self.generos)

    def shuffle (self):
        limite = self.noCancion - 1
        return self.corpus[random.randint(0,limite)]



