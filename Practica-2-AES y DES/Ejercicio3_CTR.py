from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.Util import Counter





class AES_CIPHER:
    #Bloques de 128 bits
    BLOCK_SIZE_AES = 16 

    def __init__(self,key):
        self.key = key
    
    
    def cifrar(self, cadena, contador):
        cadena = cadena.encode("UTF-8")
        cipher = AES.new(self.key, AES.MODE_CTR,counter = contador)
        ciphertext = cipher.encrypt(cadena)
        return ciphertext


    def descifrar(self, cifrado, contador):
        decipher_aes = AES.new(self.key, AES.MODE_CTR, counter=contador)
        new_data = decipher_aes.decrypt(cifrado).decode("utf-8", "ignore")
        return new_data






IV = get_random_bytes(8)
#Clave aleatoria 128 bits
key = get_random_bytes(16)
#Creo un nuevo counter
counter = Counter.new(64,prefix=IV)

print("AES Modo de Operacion CTR:")
datos = "Hola Amigos De Seguridad"
print(datos)
d = AES_CIPHER(key)
cifrado = d.cifrar(datos,counter)
print("Texto cifrado:")
print(cifrado)
descifrado = d.descifrar(cifrado,counter)
print("Texto descifrado:")
print(descifrado)






