def cifradoCesarAlfabetoIngles(cadena):
    """Devuelve un cifrado Cesar tradicional (+3)"""
    # Definir la nueva cadena resultado
    resultado = ''
    # Realizar el "cifrado", sabiendo que A = 65, Z = 90, a = 97, z = 122
    i = 0
    while i < len(cadena):
        # Recoge el caracter a cifrar
        ordenClaro = ord(cadena[i])
        ordenCifrado = 0
        # Cambia el caracter a cifrar
        if (ordenClaro >= 65 and ordenClaro <= 90):
            #Cifra los caracteres en mayusculas
            ordenCifrado = (((ordenClaro - 65) + 3) % 26) + 65
        elif (ordenClaro >= 97 and ordenClaro <= 122):
            #Cifra los caracteres en minusculas
            ordenCifrado = (((ordenClaro - 97) + 3) % 26) + 97
        # Anade el caracter cifrado al resultado
        resultado = resultado + chr(ordenCifrado)
        i = i + 1
    # devuelve el resultado
    return resultado


def descifradoCesarAlfabetoIngles(cadena):
    """Devuelve un cifrado Cesar tradicional (+3)"""
    # Definir la nueva cadena resultado
    resultado = ''
    # Realizar el "cifrado", sabiendo que A = 65, Z = 90, a = 97, z = 122
    i = 0
    while i < len(cadena):
        # Recoge el caracter a cifrar
        ordenClaro = ord(cadena[i])
        ordenCifrado = 0
        # Cambia el caracter a cifrar
        if (ordenClaro >= 65 and ordenClaro <= 90):
            #Descifra los caracteres en mayusculas
            ordenCifrado = (((ordenClaro - 65) - 3) % 26) + 65
        elif (ordenClaro >= 97 and ordenClaro <= 122):
             #Descifra los caracteres en minusculas
            ordenCifrado = (((ordenClaro - 97) - 3) % 26) + 97
        #Anade el caracter cifrado al resultado
        resultado = resultado + chr(ordenCifrado)
        i = i + 1
    #devuelve el resultado
    return resultado

def main():
    print("Introduzca un texto para realizar el cifrado Cesar:")
    texto = input()
    print(texto)
    print("Texto Cifrado")
    cifradoCESAR = cifradoCesarAlfabetoIngles(texto) 
    print(cifradoCESAR)
    print("Texto Descifrado")
    descifradoCESAR = descifradoCesarAlfabetoIngles(cifradoCESAR) 
    print(descifradoCESAR)

main()
