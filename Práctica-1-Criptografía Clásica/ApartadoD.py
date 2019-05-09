def encriptacion(texto,clave):
    #Guarda la posicion del caracter del texto para su iteraccion
    punterotexto = 0
    #Guarda la posicion del caracter de la clave para su iteraccion
    punterosecreto=0
    #Variable que define el resultado
    resuelto = ''
    
    while(punterotexto < len(texto)):
        
        enteroclaro = ord(texto[punterotexto])-65
        enterosecreto = ord(clave[punterosecreto])-64

        #Sumo uno a la iteracción del puntero del texto
        punterotexto = punterotexto + 1
        
        #Sumo uno a la iteracción del puntero de la clave y realizao el modulo por si se da
        #el caso en el que el texto sea mayor que la clave
        punterosecreto = (punterosecreto +1) % (len(clave))
        
        enteroresuelto = ((enteroclaro+enterosecreto)%26)+65
        
        #Anado el caracter al resultado
        resuelto = resuelto + chr(enteroresuelto)
        
    return resuelto

    

def desencriptacion(texto,clave):
    #Guarda la posicion del caracter del texto para su iteraccion
    punterotexto = 0
    #Guarda la posicion del caracter de la clave para su iteraccion
    punterosecreto=0
    #Variable que define el resultado
    resuelto = ''
    
    while(punterotexto < len(texto)):
        
        enteroclaro = ord(texto[punterotexto])-65
        enterosecreto = ord(clave[punterosecreto])-64

        #Sumo uno a la iteracción del puntero del texto
        punterotexto = punterotexto + 1
        
        #Sumo uno a la iteracción del puntero de la clave y realizao el modulo por si se da
        #el caso en el que el texto sea mayor que la clave
        punterosecreto = (punterosecreto +1) % (len(clave))
        
        enteroresuelto = ((enteroclaro-enterosecreto)%26)+65
        
        #Anado el caracter al resultado
        resuelto = resuelto + chr(enteroresuelto)
        
    return resuelto


def main():
    print("Introduzca el texto a cifrar en mayusculas:")
    texto = input()
    print("Introduzca la clave a usar")
    clave = input()
    print("Clave")
    textoencriptado = encriptacion(texto,clave)
    print("Texto encriptado:")
    print(textoencriptado)
    textodesencriptado = desencriptacion(textoencriptado,clave)
    print("Texto desencriptado:")
    print(textodesencriptado)
main()
