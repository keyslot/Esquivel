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
from fonetica3.div_sil import div_sil 
from fonetica3.vocal_tonica import vocal_tonica
from fonetica3.pos_tonica import pos_tonica

class Frase:
    """ 
    Clase FRASE:
    Evalua un texto, clasificando su silabas, fonetica
    """
    def __init__(self, frase):
        ' Constructor de Frase '
        self.texto = frase.lower() # una línea de texto en minúsculas
        self.longitud = len(frase) # Tamaño de caracteres
        # Obtenemos dos valores
        self.silabas, self.tamSilabas = self.contarSilabas(self.texto)
        self.fonetica = self.obtenerFonetica(self.texto)
        self.indicesFoneticos = self.asignaIndicesFoneticos()

    def asignaIndicesFoneticos(self):
        """
        Enlista índices fonéticos 
        Eje. ['amorEs'] = ['e']
        """
        l = list()
        for f in self.fonetica: 
            tonica = self.recorreFonetica(f)
            if tonica:
                l.append(tonica)
        return l

    def recorreFonetica(self,palabra):
        """
        Regresa la vocal tónica de una palabra
        """
        for i in range(0,len(palabra)):
            if palabra[i].isupper(): 
                return palabra[i].lower()
        return None

    def comparaFonetica(self,B):
        '''
        Compara la rima (ultima letra), de (A = self) con B
        '''
        A = self.recorreFonetica(self.fonetica[-1])
        B = self.recorreFonetica(self.obtenerFonetica(B)[-1])
        return True if A == B else False

    def contarSilabas(self,cadena):
        '''
        Cuentra la silabas, regresa un vector 
        demostrativo de la separación en silabas,
        y un contador de cuantas silabas hay en la cadena.
        Uso de div_sil
        '''
        silabas = list()
        contador = 0
        for x in cadena.split(' '): 
            if x and x != ' ':
                y = div_sil(x)
                # Procesamos la salida y de div_sil de x
                contador += len(y.split ('.'))
                silabas.append(y)
        return silabas,contador

    def obtenerFonetica(self,cadena):
        '''
        Obtiene la fonética de una cadena
        acorde a la vocal tónica de cada palabra
        regresa una vector.
        Uso de vocal_tonica
        '''
        fonetica = list()
        for x in cadena.split(' '):
            if x and x != ' ':
                y = vocal_tonica(x)
                fonetica.append(y)
        return fonetica


