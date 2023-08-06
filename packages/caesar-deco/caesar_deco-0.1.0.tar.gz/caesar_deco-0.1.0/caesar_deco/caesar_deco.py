# -*- coding: utf-8 -*-

"""Main module."""
import string
import numpy as np

def caesar_decoder(texto):
    soluciones=[]
    vector_texto=list(texto)
    #se genera el abcdario
    abc=string.ascii_lowercase[:26]
    #se convierte a un vector
    abcd=list(abc)
    #se genera un vector vacio en el cual se almacenara el nuevo abecedario segun el corrimiento
    nuevo_abcd=[]
    #posicion_izquierda2 variable  inicio cuando el vector abcd llega a la letra "z" 
    posicion_izquierda2=0
    #print ("corrimientos a izquierda")
    espacio=" "
    vector_abcd=[]

    #se genera el nuevo conjunto de 26 abecedarios, por ejemplo el primero tiene corrimiento de 1 con respecto al original,
    #el segundo tiene corrimiento de 2 con respecto al original y asi sucesivamente
    for corrimiento in range (len(abcd)):
        nuevo_abcd=[]
        for i in range(len(abcd)):
            posicion=i+corrimiento
            if (posicion<26):
                letra=abcd[posicion]
                nuevo_abcd.append(letra)
                posicion_izquierda2=0
            elif(posicion>25):
                letra=abcd[posicion_izquierda2]
                nuevo_abcd.append(letra)
                posicion_izquierda2=posicion_izquierda2+1
        vector_abcd.append(nuevo_abcd)

    # se compara el texto ingresado con cada uno de los abededarios generados, para luego agregar al vector mensaje 
    #los posibles resultados de la frase encriptada
    for k  in range (len(vector_abcd)):  
        nuevo_abcd=vector_abcd[k]
        mensaje=[]
        for l in range(len(vector_texto)):
            for j in range(len(nuevo_abcd)):
                if (vector_texto[l]==abcd[j]):
                    mensaje.append(nuevo_abcd[j])
                #esto es para separar las palabras
                elif (vector_texto[l]==espacio):
                    mensaje.append(espacio)
        #a continuacion se buscara imprimir en pantalla los posibles mensajes de una manera mas organizada
        caracteres=""
        #se crea una cadena de caracteres con el posible mensaje 
        for f in range (len(mensaje)):
            a=mensaje[f]
            caracteres=caracteres+a
        #como la cadena de caracteres contiene palabras muy espaciadas entre si, se procede a eliminar dichos espacios
        cadena_espacios=caracteres.split(' ')
        cadena=[]
        #se crea un vector de palabras
        for m in range(len(cadena_espacios)):
            if ((m==0))|((m%26==0)):
                cadena.append(cadena_espacios[m])
        #se separan las palabras
        caracteres=""
        for n in range(len(cadena)):
            b=cadena[n]
            caracteres=caracteres+b+espacio
        
        soluciones.append(caracteres)
    soluciones=np.asarray(soluciones)
    soluciones=soluciones.transpose()
    return print(soluciones)
    
