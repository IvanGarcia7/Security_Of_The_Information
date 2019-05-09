from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad





class AES_CIPHER:

    #Defino un bloque de 128 bits
    BLOCK_SIZE_AES = 16 

    def __init__(self,key):
        self.key = key

    
    def cifrar(self, cadena, IV):
        cadena = cadena.encode("UTF-8")
        # Creamos un mecanismo de cifrado AES en modo CBC con una inicializacion IV
        cipher = AES.new(self.key, AES.MODE_CBC, IV)
        # Ciframos, haciendo que data sea multiplo del tamaño de bloque
        ciphertext = cipher.encrypt(pad(cadena,self.BLOCK_SIZE_AES))
        return ciphertext


    def descifrar(self, cifrado, IV):
        # Creamos un mecanismo de (des)cifrado AES en modo CBC con una inicializacion IV
        # Ambos, cifrado y descifrado, se crean de la misma forma
        decipher_aes = AES.new(self.key, AES.MODE_CBC, IV)
        # Desciframos, eliminamos el padding, y recuperamos la cadena
        new_data = unpad(decipher_aes.decrypt(cifrado), self.BLOCK_SIZE_AES).decode("utf-8", "ignore")
        return new_data


    



#IV aleatorio 128 bits
IV = get_random_bytes(16)
#Clave aleatoria 128 bits
key = get_random_bytes(16)

datos = "Hola mundo con AES en modo CBC"
print(datos)

d = AES_CIPHER(key)
cifrado = d.cifrar(datos, IV)
print("Texto cifrado:")
print(cifrado)
descifrado = d.descifrar(cifrado, IV)
print("Texto descifrado:")
print(descifrado)






