'''
-----------------------  E S Q U I V E L --------------------------------
    Titulo, honor a Juan Garcia Esquivel
    Info: Generativa automática de canciones (Experimento)
    Autor: Raúl Antonio Ortega Vallejo
-------------------------------------------------------------------------
    Bibliotecas requeridas por el programa 
-------------------------------------------------------------------------
    Uso de la biblioteca: 'fonetica3':
    Autor: Carlos Daniel Hernandez Mena 
    https:/github.com/CarlosDanielMena/Libreria_Fonetica3
-------------------------------------------------------------------------
'''
import csv    # Formato de Salida del Corpus (Inspiración del programa)
import random # Procesos aleatorios
import unicodedata #Acentos
import pickle # Seriabilizacion
from sys import argv # Argumentos from shell
from collections import defaultdict # Diccionarios de Listas
from frase import * # Clase Frase
from corpus import * # Claee Corpus
from time import sleep # Delay
from datetime import datetime # Timestamp
from os import path, makedirs # Directorios
' Bibliotecas para la Interfaz GUI '
from tkinter.ttk import Progressbar
from tkinter import Tk,Text,Label,Entry,filedialog,\
                    Toplevel,BooleanVar,Checkbutton,Button, HORIZONTAL,END
            
class Esquivel:

    '''
    Clase Esquivel - Motor del programa:
         - Dispone de interfaz tkinter
         - Procesa el corpus (inspiración A de la generativa)
         - Procesa el input (inspiración B de la generativa)
         - Seriabiliza objetos
         - Crea una canción (procesa el output)
    '''

    def __init__(self):
        ' Constructor de un Esquivel '
        self.corpus = None # Corpus del programa
        self.input = None  # INPUT
        self.output = None # OUTPUT
        self.limiteSilabas = 0 # Limite de silabas
        self.limiteFrases = 0 # Limite de silabas
        self.estribillo = "Generativa de Canciones"
        ''' 
        Directorios de los ficheros del programa
        '''
        self.direCorpus  = "Corpus/2019_letras_es" # Archivo corpus (csv)
        self.direOutput  = "Output/" # Canciones generadas 
        self.direObjetos = "Objetos/Clase_Corpus_Objeto.pickle" # Objeto tipo Corpus 


    def mostrarCorpus(self):
        '''
        Imprime el corpus en el shell
        '''
        print("iniciando ...")
        self.cargarCorpus()
        self.corpus.iterar()
        self.liberarMemoria()

    def liberarMemoria(self):
        '''
        Salida = Cerrar la interfaz:
        Limpieza de variables
        '''
        print("Liberando memoria")
        if self.corpus: 
            self.corpus.destruir()
        if self.input:
            self.input.clear()
        if self.output:
            del self.output

    def serializarCorpus(self):
        self.liberarMemoria()
        direObjetos = self.direObjetos.split("/") [0] 
        if not path.exists (direObjetos):
            makedirs(direObjetos)
            print("Directorio creado:", direObjetos)
            del direObjetos
        print("Serializando el corpus, por favor espere...")
        self.corpus = Corpus(self.direCorpus)
        print("Grabando Clase Corpus")
        try:
            with open(self.direObjetos, 'wb') as handle:
                pickle.dump(self.corpus, handle, protocol = pickle.HIGHEST_PROTOCOL)
            print("Corpus grabado")
        except:
            print("Error al intentar serializar el corpus")

    def cargarCorpus(self):
        '''
        Lectura de un objeto serializado, del tipo clase Corpus
        '''
        try:
            with open(self.direObjetos, 'rb') as handle:
                self.corpus = pickle.load(handle)
                print ('Corpus cargado')
        except:
            print("No se encontró el objeto tipo Corpus: ", self.direObjetos)
            self.serializarCorpus()


    def experimentar(self):
        '''
        Método para experimentar, eligiendo al azar una canción y analizarla
        '''
        print ("Experimentando")
        separador = '>' * 100 # Separador visual
        agitar = self.corpus.shuffle()
        self.mostrarAccion("Titulo: %s" % (agitar['titulo']))
        self.mostrarAccion(self.separador)
        self.mostrarAccion("Letra: \n%s" % (agitar['letra']))
        print ("Lineas: ",len(agitar['letra']))
        self.mostrarAccion(separador)
        print ("FRASES:")
        f = set()
        frases = list()
        for dic in agitar['letra']: f.add(dic)
        self.mostrarAccion("%s\nFrases: %s" % (f,len(f)))
        i = 0
        for frase in f:
            i += 1
            nueva = Frase(frase)
            self.mostrarAccion("|Frase: %d| %s |\nSILABAS:%s = %d\nFONÉTICA:%s\n" % \
                    (i, nueva.texto,nueva.silabas,nueva.tamSilabas,nueva.fonetica))

    def procesarInput(self):
        '''
        Procesamiento del input,entrada: el programa supone un archivo.txt
        '''
        def ajustarFrase(x):
            '''
            Función propia del método procesarInput
            Recorta la frase, acorde a los parametros
            configurados por el usuario
            '''
            test = Frase(x)
            # Debug: imprimimos índices fonéticos
            # print(test.indicesFoneticos)
            ' Rango de 2, para evitar un alta restrincción ' 
            if self.limiteSilabas > 2:
                op = test.tamSilabas - self.limiteSilabas
                # Mientras se rebase el límite, corta la frase por palabra
                while op > 0:
                    y = test.texto.split(' ')
                    y.pop()
                    y = "".join([i + " " for i in y]) [:-1]
                    test = Frase(y)
                    op = test.tamSilabas - self.limiteSilabas
            # Regresamos el objeto de tipo Frase
            return test
            
        self.mostrarAccion("Procesando input...")
        # Obtenemos el input - text box, de entrada
        texto = self.elementos['input']
        # Obtenemos el limite de Silabas
        limiteSilabas  = self.elementos['inputSilabas'].get()
        # Obtenemos el limite de frases
        limiteFrases = self.elementos['inputFrases'].get()
        # Si existe un límite de Silabas
        if len(limiteSilabas) > 0:
            self.limiteSilabas = int(limiteSilabas)
            self.mostrarAccion("Limite de silabas por frase %s" % (limiteSilabas))
            sleep(1)
        # Si existe un lítimi
        if len(limiteFrases) > 0:
            self.limiteFrases = int(limiteFrases)
            self.mostrarAccion("Limite de silabas por frase %s" % (limiteFrases))
            sleep(1)
        # Tomamos las frases del input
        frases = texto.get("1.0",END)
        # Configuramos temporalmente la edición del text box
        texto.config(state = 'normal')
        # Limpiamos el textbox
        texto.delete("1.0", END)
        # Creamos el correcto input que utilizará el programa
        self.input = list()
        '''
        IMPORTANTE:
        Revisar las condiciones del input, ya que el programa
        separa por saltos de línea casa Frase, para su procesamiento
        '''
        frases = frases.split('\n')[:-1] #Evitamos el último salto
        n = 0 # Contador de frases procesadas
        for x in frases:
            if  2 < self.limiteFrases <= n: break
            if x and x != ' ':
                y = ajustarFrase(x)
                texto.insert(END, y.texto + "\n")
                self.master.update()
                self.input.append(y)
                n += 1
        # Volvemos a deshabilitar el text box
        texto.config(state = 'disabled')
        # Contador (PORCENTAJE) para incrementar la barra de proceso
        self.proceso = 100/n 
    
    def generarCanciones(self):
        salida = list()
        '''
        -----------  Funciones propias del Metodo generarCanciones --------------------
        '''
        def regresarFrase(arreglo):
            '''
            Regresa un objeto de tipo Frase, acorde a un arreglo
            '''
            frase = None
            # Nos aseguramos de que los inidices existen
            try: frase = Frase(self.corpus.corpus[arreglo[0]]['letra'][arreglo[1]])
            # Error...
            except: pass
            return frase

        def foneticaAceptable(a,b,maximo = None):
            '''
            Evalua la fonetica, ponderando la diferencia entre las frases A y B
            True|False
            '''
            diferencia = 0
            if not maximo: 
                maximo = 2
            a = a.indicesFoneticos 
            b = b.indicesFoneticos
            for i in range(0, len(a)):
                # Intentamos acceder al inidiceis de los strings a, b
                try:
                    if a[i] != b[i]:
                        diferencia += 1
                except: pass
            # Regresamos el booleano
            return True if maximo > diferencia else False

        def evaluarRango(a,b):
            '''
            Evalua la ultima palaba ritmica de a y b
            Comparando las últimas letras que las complementan
            '''
            # Tratamos de acceder a los inidices
            try: 
                accion = "Evaluando la rima de '%s' con '%s' " % (a,b)
                self.mostrarAccion(accion)
                ' Evaluamos si la palabra tiene signos al final '       
                if a[-1] == '?' or a[-1] == '!' or a[-1] == '.' or a[-1] == ',' :
                    a = a[:-1] #Descartamos el signo
                if a[-2:] == b[-2:] or a[-3:] == b[-3:] or a[-4:] == b[-4:]:
                    return True
            except: pass
            return False
              
        def elegirCandidato(x,listaCandidatos):
            '''
            Elige un candidato óptimo de la lista
            '''
            self.mostrarAccion("Eligiendo candidato")
            destacados =  list() # Contiene candidatos destacados
            rango = -3 # Posicion Desde la ultima palabra 
            a = x.texto.split(' ')[-1] # separamos y obtemos última palabra de x
            for n in listaCandidatos:
                b = regresarFrase(n)
                c = b.texto.split(' ')[-1] 
                try:
                    '''
                    Evaluamos:
                    - Fonetica Aceptable (Tonicas)
                    - Que la últimas palabras de 'a' y 'b' no sean iguales
                    - La ultimas letras (rango) sean semejantes 
                    ''' 
                    if foneticaAceptable(x, b, 4) and a != c and evaluarRango(a,c):
                       accion = "MATCH: Encontrado un alto candidato: %s" % (b.texto)
                       self.mostrarAccion(accion)
                       destacados.append(n)
                       del b  # Liberamos memoria
                       sleep(0.1)
                except: pass
            if destacados: # Existen candidatos destacados:
               # Elegimos al azar 
               candidato = destacados [random.randint(0, len(destacados) - 1)]
               destacados.clear() # Limpieza
               return candidato
            else: 
                ' No hay destacados,elegimos al azar una frase, y evaluamos la fonetica '
                accion = ">> No se encontraron candidatos destacados para '%s'" % (x.texto)
                self.mostrarAccion(accion)
                sleep(1)
                # 30 intentos para buscar match
                posibles = len(listaCandidatos)
                for intento in range(0, posibles):
                    # Elegimos al azar 
                    candidato = listaCandidatos [random.randint(0, posibles - 1)]
                    y = regresarFrase(candidato)
                    self.mostrarAccion("Buscando más opciones, intento %d" % (intento + 1))
                    sleep(0.5)
                    # Damos una mayor flexibilidad al rango aceptable de la fónetica
                    if (foneticaAceptable(x,y)):
                        del y
                        return candidato
            # Intentos Fallidos...
            # No encontramos nada
            return None
        def comparar(rima, silabas, x):
            '''
            Compara  la rima y las silabas
            '''
            candidato = None
            candidatos = None
            if rima and silabas:
                try:
                    candidatos = self.corpus.mapeo[rima,silabas]
                except:
                    print ("Error al intentar acceder al mapeo de %s, %s" % (rima,silabas))
                'Debemos evaluar si no existen candidatos'
                if candidatos: # Si existen candidatos:
                    opcion = elegirCandidato(x, candidatos) # Elegimos uno
                    if opcion:
                        candidato = regresarFrase(opcion)
                        return candidato, opcion[0]
            'Error del programa, regresamos NULL, NULL'
            return None, None

        def encontrarEstribillo (fonetica,rima):
            if self.elementos['botonEstribillo'].get():
                contador = 0
                for vocal in fonetica:
                    if  rima == vocal: contador += 1
                self.estribillo[rima] = contador

        def procesarEstribillo(fraseIntermedia):
            '''
            Procesar estribillo
            Ordena por frecuencia la vocal tónica, y toma la de mayor aparición
            '''
            if self.elementos['botonEstribillo'].get():
                candidato = None
                try :
                    indice = sorted(self.estribillo.items(), key = lambda llave:llave[1], reverse = True)
                    vocal = indice[0][0] # Tomamos la mayor (first)
                    candidatos = self.corpus.mapeo[vocal, fraseIntermedia.tamSilabas]
                    candidato = elegirCandidato(fraseIntermedia, candidatos)
                except:
                    print ("Error al procesar estribillo")
                if candidato:
                    frase = regresarFrase(candidato)
                    # Actualizamos el valor del estribillo
                    self.estribillo = frase.texto
                    rima = frase.indicesFoneticos[-1]
                    return [self.estribillo, rima]

        def ajustarSalida(salida):
            '''
            Ajustamos la salida de la canción
            '''
            # Reparación de Mayúsuclas
            mayus = salida[0].upper()
            mayus +=  salida[1:]
            # Agregamos un salto de linea
            self.output += mayus + "\n"
            # Debug
            # print(mayus)
            
        def inspirarEstribillo(fraseIntermedia):
            '''
            Inspiramos el estribillo base una frase intermedia.
            '''
            if self.elementos['botonEstribillo'].get():
                # Obtenemos el estribillo ya evaluado y procesado 
                accion = ('>' * 50) + "Procesando estribillo"
                self.mostrarAccion(accion)
                estribillo = procesarEstribillo(fraseIntermedia)
                '''
                Justificación de los resultados
                para la generación del estribillo:
                '''
                self.mostrarAccion(str(estribillo))
                self.mostrarAccion(str(estribillo))
                ajustarSalida(estribillo[0])
                ajustarSalida(estribillo[0])

        # Comprobamos si el usuario desea crear un estribillo
        if self.elementos['botonEstribillo'].get() : 
            self.estribillo = defaultdict(list)

        for n in self.input:
            candidato = None
            try:
                tam  = n.tamSilabas 
                rima = n.indicesFoneticos[-1]
                candidato, cancion = comparar(rima, tam, n)
                salida.append([n.texto, n.indicesFoneticos[-1]])
            except: 
                self.mostrarAccion("¡Input demasiado corto!")
            if candidato:
                salida.append([candidato.texto,[cancion, rima, tam]])
                encontrarEstribillo(candidato.indicesFoneticos, rima)
                # Limpieza de memoria
                del candidato # Borramos el objeto tipo clase
            else:
                # FALLA DEL PROGRAMA
                falla = ["El programa no tuvo inspiracion para la frase"]
                self.mostrarAccion(str(falla))
                salida.append(falla)
            self.actualizarBarraProceso()
            
        '''
        Generación de canciones terminada
        '''
        mensajeFinal = ('>' * 50) + " Generacion Terminada"
        self.mostrarAccion(mensajeFinal)
        sleep(0.1)
        # Preparamos el tipo de dato para la canción
        self.output = ''

        # Encontrar frase intermedia
        intermedia = len(salida) / 2
        i = 0
        for y in salida:
            i += 1
            #print(y)
            self.mostrarAccion(str(y))
            ajustarSalida (y[0])
            if i == intermedia :
                fraseIntermedia = Frase(y[0])
                inspirarEstribillo (fraseIntermedia)
        salida.clear()
        self.finalizarGenerativa()

    def reiniciarMotor(self):
        '''
        Destruye la ventana, 
        crea otra instancia del programa
        '''
        self.master.destroy();
        reinicia = Esquivel()
        reinicia.ejecutar()

    def finalizarGenerativa(self):
        '''
        Finalizamos la generativa de canciones
        '''
        # Experimental
        nuevaVentana = Toplevel()
        nuevaVentana.geometry("800x450+10+10")
        nuevaVentana.title(self.estribillo)
        textoInput = Text(nuevaVentana)
        textoInput.place(x = 10, y = 10, width = 760, height = 340) 
        textoInput.insert(END,self.output)
        textoInput.config(state = "disabled")
        # Guardamos la cancion
        if self.guardarCancion():
            mensaje = "Cancion '%s' guardada en : %s" \
                    % (self.estribillo,self.direOutput)
            Label(nuevaVentana, text = mensaje).place(x = 10, y = 370)

        nuevaVentana.transient(self.master)
        nuevaVentana.grab_set()
        botonReIniciar = Button(self.master,text='REINICIAR PROGRAMA',command=self.reiniciarMotor)
        botonReIniciar.place(x = 550, y = 310)

        
    def actualizarBarraProceso(self,porcentaje=None):
        '''
        Actualiza la barra de proceso 
        '''
        status = self.elementos['barraProceso']
        status['value'] += self.proceso
        status.update_idletasks()

    def mostrarAccion(self,accion):
        '''
        Muestra en interfaz, la tupla de acciones
        realizadas por el programa
        '''
        try:
            acciones = self.elementos['acciones']
            acciones.insert(END,accion + '\n')
            # Apuntar el cursor al final
            acciones.see(END)
            # Actualizar la interfaz
            self.master.update()
        except: pass
        return
        # DEBUG
        #print(accion)

    def deshabilitarElemento(self, elemento):
        elemento.config(state = 'disabled')
            
    def validarInput(self):
        self.mostrarAccion("Validando input...")
        entrada = self.elementos['input']
        # Validamos el input text box para la entrada
        if entrada.compare("end-1c", "==", "1.0"):
            self.mostrarAccion(">> Error, se requiere un input")
            return False
        return True

    def preprocesarInput(self):
        if self.validarInput():
            '''
            Procesamos el input
            '''
            self.procesarInput()
            self.elementos['input'].config(state = 'normal')

    def iniciarMotor(self):
        # Evaluamos el input
        if self.validarInput():
            '''
            Inicia el programa
            '''
            self.procesarInput()
            self.deshabilitarElemento(self.elementos['input'])
            self.deshabilitarElemento(self.elementos['botonIniciar'])
            self.deshabilitarElemento(self.elementos['botonArchivo'])
            self.deshabilitarElemento(self.elementos['botonPreprocesar'])
            self.mostrarAccion("INICIANDO EL PROGRAMA")
            self.generarCanciones()

    def solicitarArchivo(self):
        '''
        Solicitamos un archivo para el input
        '''
        entrada = self.elementos['input']
        try:
            dialogoPeticion = filedialog.askopenfilename(title = "Seleccionar archivo")
            with open(dialogoPeticion, "r") as archivo:
                 entrada.insert(END,archivo.read())
        except Exception as e: 
            print(">> Error de lectura en archivo: ", e)

    def guardarCancion(self):
        '''
        Guarda una canción generada por el programa
        sólo si se pudo generar una salida
        '''
        if self.output:
            try:
                if not path.exists (self.direOutput):
                    makedirs(self.direOutput)
                    print("Directorio creado:", self.direOutput)
                '''
                Guardamos la canción generada
                En extensión 'txt', timestamp como nombre de origen. 
                '''
                self.direOutput += str(datetime.now()) + '.txt'
                with open(self.direOutput, "w") as archivo:
                    # Grabamos título,
                    archivo.write ('>' * 50 + " Título: " +   self.estribillo  + "\n")
                    # Grabamos canción
                    archivo.write(self.output)
                    # Grabamos timestamp
                self.mostrarAccion("Cancion guardada")
                return True
            except:
                print("Error al tratar de guardar la cancion")
        return False
    
    def ejecutar(self):
        '''
        Ejecuta la interfaz del proyecto Esquivel
        Arracna el corpus, inicia la generativa de canciones
        '''
        self.cargarCorpus()
        '''
        Atributos de la ventana GUI
        '''
        self.master = Tk()
        # Ventana color blanco
        self.master.configure(background = 'white')
        # Geometría
        self.master.geometry("800x510+10+10")
        # Elementos de la ventana
        self.elementos = None # Elementos de la GUI
        self.proceso = 0 # Incrementa la barra proceso
        # Titulo del programa
        if not self.corpus:
            print("Se requiere cargar el corpus")
        else: 
            mensaje = "Generativa de Canciones - Esquivel"
            print(mensaje)
            self.master.title(mensaje)
            '''
            Elementos de la interfaz GUI
            '''
            self.elementos =  {}
            # Mostramos el bloque de texto para editar el input
            textoInput = self.elementos['input'] = Text(self.master)
            textoInput.place(x = 10, y = 25, width=500, height= 300) 
            textoAcciones = self.elementos['acciones'] =  Text(self.master)
            textoAcciones.place(x = 10,  y = 350, width = 750, height = 90)
            '''
            Mostramos los Labels 
            '''
            Label(self.master, text = "CONFIGURACIÓN").place(x = 550, y = 10)
            Label(self.master, text = "INSPIRACIÓN - INPUT").place(x = 10, y = 5)
            # Numero de Silabas
            Label(self.master, text = "Límite de Silabas > 2:").place(x = 550, y = 30)
            Label(self.master, text = "Límite de Frases  > 2:").place(x = 550, y = 60)
            # Acciones del programa
            Label(self.master, text = "ACCIONES DEL PROGRAMA").place(x = 10, y = 330)
            Label(self.master, text = "STATUS").place(x = 10, y = 450)
            '''
            Campos de Entrada - Input
            '''
            inputSilabas = self.elementos['inputSilabas'] =  Entry(self.master)
            inputSilabas.place(x = 700, y = 30, width = 30, height = 20)
            inputFrases = self.elementos['inputFrases'] =  Entry(self.master)
            inputFrases.place(x = 700, y = 60, width = 30, height = 20)
            '''
            Botones
            '''
            botonEstribillo = self.elementos['botonEstribillo'] = BooleanVar()
            Checkbutton(self.master, text='Generar estribillo', \
                    var = botonEstribillo).place(x = 550, y = 100)
            # Cargar input (archivos de texto plano)
            botonArchivo = self.elementos['botonArchivo'] =\
                    Button(self.master,text='Importar narrativa',command=self.solicitarArchivo)
            botonArchivo.place(x = 550, y = 130)
            # Procesar input
            botonIniciar = self.elementos['botonPreprocesar'] =\
                    Button(self.master,text='PREPROCESAR',command=self.preprocesarInput)
            botonIniciar.place(x = 550, y = 180)
            # Boton para iniciar el programa
            botonIniciar = self.elementos['botonIniciar'] =\
                    Button(self.master,text='INICIAR PROGRAMA',command=self.iniciarMotor)
            botonIniciar.place(x = 550, y = 250)
            '''
            Otros elementos
            '''
            # Barra de proceso
            status = self.elementos['barraProceso'] =\
                    Progressbar(self.master,orient=HORIZONTAL,length=100,mode='determinate')
            status.place(x = 10, y = 470, width = 200)
            # Boton reiniciar 

            # Loop de Tkinter
            self.master.mainloop()

        '''
        El usuario cierra la ventana
        '''
        self.liberarMemoria()


    def iniciar (self):
        "Configuramos el menu"
        menu = {1:["Mostrar copus", self.mostrarCorpus],# KEY, [Descripción , Funcion]
                2:["Iniciar interfaz", self.ejecutar],
                3:["Salir", exit]}
        while 1:
            print (">>>>>>  ESQUIVEL <<<<<<")
            print ("------ M E N U ------")
            for tecla,funcion in menu.items(): # Imprime el Menú
                print ("[%s] %s"%(tecla,funcion[0])) # Muestra las teclas
            try: 
                eleccion = int(input("_"))
                if eleccion in menu:
                    print (">>> %s...\n"%menu[eleccion][0])
                    menu[eleccion][1]() # Ejecuta la función seleccionada del menú
            except Exception as e: print (e)


'''
------------- MAIN -----------------
'''
def main():
    programa = Esquivel()
    programa.iniciar()

if __name__ == '__main__':
    main()
