from Crypto.Random import get_random_bytes
from Crypto.Cipher import DES, AES
from Crypto.Util.Padding import pad,unpad





class DES_CIPHER:

    #Defino un bloque de 64 bits
    BLOCK_SIZE_DES = 8 

    def __init__(self,key):
        self.key = key

    
    def cifrar(self, cadena, IV):
        cadena = cadena.encode("UTF-8")
        # Creamos un mecanismo de cifrado DES en modo CBC con una inicializacion IV
        cipher = DES.new(self.key, DES.MODE_CBC, IV)
        # Ciframos, haciendo que data sea multiplo del tamaño de bloque
        ciphertext = cipher.encrypt(pad(cadena,self.BLOCK_SIZE_DES))
        return ciphertext


    def descifrar(self, cifrado, IV):
        # Creamos un mecanismo de (des)cifrado DES en modo CBC con una inicializacion IV
        # Ambos, cifrado y descifrado, se crean de la misma forma
        decipher_des = DES.new(self.key, DES.MODE_CBC, IV)
        # Desciframos, eliminamos el padding, y recuperamos la cadena
        new_data = unpad(decipher_des.decrypt(cifrado), self.BLOCK_SIZE_DES).decode("utf-8", "ignore")
        return new_data


    


#IV aleatorio 64 bits
IV = get_random_bytes(8)
#Clave aleatoria 64 bits
key = get_random_bytes(8)

datos = "Hola mundo con DES en modo CBC"
print(datos)

d = DES_CIPHER(key)

cifrado = d.cifrar(datos, IV)
print("Texto cifrado:")
print(cifrado)
descifrado = d.descifrar(cifrado, IV)
print("Texto descifrado:")
print(descifrado)






