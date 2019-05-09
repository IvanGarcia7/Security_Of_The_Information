from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pss
from Crypto.Hash import SHA256

class RSA_OBJECT:

   #Defino la longitud
    KEY_LENGTH = 2048
    public_key = None
    private_key = None


    def __init__(self):
        #Inicializa un objeto RSA, sin ninguna clave
        # Nota: Para comprobar si un objeto (no) ha sido inicializado, hay
        #   que hacer "if self.public_key is None:" 
        #Si ha sido inicializado previamente, defino ambas claves como None
        if self.public_key is None:
            self.private_key = None
       

    def create_KeyPair(self):
        #Crea un par de claves publico/privada, y las almacena dentro de la instancia
        self.private_key = RSA.generate(self.KEY_LENGTH)
        self.public_key = self.private_key.publickey()
       

    def save_PrivateKey(self, file, password):
        #Guarda la clave privada self.private_key en un fichero file, usando una contraseña password
        key_cifrada = self.private_key.export_key(passphrase=password, pkcs=8,protection="scryptAndAES128-CBC")
        file_out = open(file, "wb")
        file_out.write(key_cifrada)
        file_out.close()


    def load_PrivateKey(self, file, password):
        #Carga la clave privada self.private_key de un fichero file, usando una contraseña password
        key_cifrada = open(file, "rb").read()
        self.private_key = RSA.import_key(key_cifrada, passphrase=password)


    def save_PublicKey(self, file):
        #Guarda la clave publica self.public_key en un fichero file
        key_pub = self.public_key.export_key()
        file_out = open(file, "wb")
        file_out.write(key_pub)
        file_out.close()

    def load_PublicKey(self, file):
        #Carga la clave publica self.public_key de un fichero file
        key_publica = open(file, "rb").read()
        self.public_key = RSA.import_key(key_publica)

    def cifrar(self, datos):
        #Cifra el parámetro datos (de tipo binario) con la clave self.public_key, y devuelve
        #el resultado. En caso de error, se devuelve None
        if(self.public_key is None):
            return None
                
        engineRSACifrado = PKCS1_OAEP.new(self.public_key)
        cifrado = engineRSACifrado.encrypt(datos)
        return cifrado
        

    def descifrar(self, cifrado):
        #Descrifra el parámetro cifrado (de tipo binario) con la clave self.private_key, y devuelve
        #el resultado (de tipo binario). En caso de error, se devuelve None
        if(self.private_key is None):
            return None

        
        engineRSADescifrado = PKCS1_OAEP.new(self.private_key)
        datos = engineRSADescifrado.decrypt(cifrado)
        return datos
        
        


    def firmar(self, datos):
        #Firma el parámetro datos (de tipo binario) con la clave self.private_key, y devuelve el 
        #resultado. En caso de error, se devuelve None.
        try:
            h = SHA256.new(datos)
            print("\nFirma:")
            print(h.hexdigest())
            signature = pss.new(self.private_key).sign(h)
            return signature
        except (ValueError, TypeError):
            return None

    def comprobar(self, text, signature):
        #Comprueba el parámetro text (de tipo binario) con respecto a una firma signature 
        #(de tipo binario), usando para ello la clave self.public_key. 
        #Devuelve True si la comprobacion es correcta, o False en caso contrario o 
        #en caso de error.

        h = SHA256.new(text)
        print("\nFirma:")
        print(h.hexdigest())
        verifier = pss.new(self.public_key)
        try:
            verifier.verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False

class AES_CIPHER:

    #Bloque 128 bits
    BLOCK_SIZE_AES = 16 

    def __init__(self,key):
        self.key = key

    
    def cifrar(self, cadena, IV):
        cadena = cadena.encode("UTF-8")
        # Creamos un mecanismo de cifrado AES en modo CFB
        cipher = AES.new(self.key, AES.MODE_CFB,IV)
        # Ciframos, haciendo que data sea multiplo del tamaño de bloque
        ciphertext = cipher.encrypt(pad(cadena,self.BLOCK_SIZE_AES))
        return ciphertext


    def descifrar(self, cifrado, IV):
        # Creamos un mecanismo de (des)cifrado ECB en modo CFB
        # Ambos, cifrado y descifrado, se crean de la misma forma
        decipher_aes = AES.new(self.key, AES.MODE_CFB, IV)
        # Desciframos, eliminamos el padding, y recuperamos la cadena
        new_data = unpad(decipher_aes.decrypt(cifrado), self.BLOCK_SIZE_AES).decode("utf-8", "ignore")
        return new_data



# Main
# =PROTOCOLO A SEGUIR=
#Primero por parte de A, cifro el mensaje con la clave publica de B
#Firmo dicho mensaje con la clave privada de A
#Escribo en un fichero el mensaje
#Leo el mensaje del fichero
#Compruebo la firma con clave publica de A cifrado y firma
#Si se cumple el paso anterior descifro el texto con la clave privada de B

# Crear claves RSA del usuario A
# y guardar en ficheros la clave privada (protegida) y publica
passwordA = "passwordA"
private_fileA = "rsa_keyA.pem"
public_fileA = "rsa_keyA.pub"
RSA_key_creatorA = RSA_OBJECT()
RSA_key_creatorA.create_KeyPair()
RSA_key_creatorA.save_PrivateKey(private_fileA, passwordA)
RSA_key_creatorA.save_PublicKey(public_fileA)


# Crear claves RSA del usuario B
# y guardar en ficheros la clave privada (protegida) y publica
passwordB = "passwordB"
private_fileB = "rsa_keyB.pem"
public_fileB = "rsa_keyB.pub"
RSA_key_creatorB = RSA_OBJECT()
RSA_key_creatorB.create_KeyPair()
RSA_key_creatorB.save_PrivateKey(private_fileB, passwordB)
RSA_key_creatorB.save_PublicKey(public_fileB)

# Crea dos clases, una con la clave privada y otra con la clave publica para A
RSA_privateA = RSA_OBJECT()
RSA_publicA = RSA_OBJECT()
RSA_privateA.load_PrivateKey(private_fileA, passwordA)
RSA_publicA.load_PublicKey(public_fileA)


# Crea dos clases, una con la clave privada y otra con la clave publica para B
RSA_privateB = RSA_OBJECT()
RSA_publicB = RSA_OBJECT()
RSA_privateB.load_PrivateKey(private_fileB, passwordB)
RSA_publicB.load_PublicKey(public_fileB)




#Defino como mensaje a intercambiar una clave de AES de 128 bits
mensaje = get_random_bytes(16)

#Cifro y firmo el mensaje con el protocolo definido
cifrados = RSA_publicB.cifrar(mensaje)
print("Mensaje cifrado RSA:")
print(cifrados)
print("Tamano del mensaje:")
print(len(cifrados))

firmas =RSA_privateA.firmar(cifrados)

fichero = "canal.txt"

#Escribo en un fichero simulando el intercambio del mensaje
file_out = open(fichero, "wb")
file_out.write(firmas)
file_out.write(cifrados)
file_out.close()

#Abro el fichero para leer el mensaje y la firma
ficherodos = open(fichero, "rb")
firmados = ficherodos.read(256)
cifradodos = ficherodos.read()


if RSA_publicA.comprobar(cifradodos, firmados):
    key = RSA_privateB.descifrar(cifradodos)
    #print("Clave intercambiada:")
    #print(key)
    IV = get_random_bytes(16) # IV aleatorio de 128 bits
    #print("Mensaje a enviar")
    datos = "Hola amigos de seguridad"
    #print(datos)
    d = AES_CIPHER(key)
    cifrado = d.cifrar(datos, IV)
    print("\nMensaje cifrado AES:")
    print(cifrado)
    print("Tamano del mensaje:")
    print(len(cifrado))
    e = AES_CIPHER(key)
    descifrado = e.descifrar(cifrado, IV)
    print("\nMensaje descifrado:")
    print(descifrado)
else:
    print("La firma es invalida")




#La longitud del mensace cifrado utilizando RSA es de 256 bytes,
#En cambio con AES genera un mensaje de 32 bytes
#La principal diferencia entre ambos mensajes cifrados por tanto corresponde al tamaño
#de los mismos, el cual depende directamente del tamaño de la clave.
#RSA es asimétrico y lento, en comparación con AES el cual es simétrico y veloz.
#El tamaño de las claves requerido en el cifrado simétrico es siempre menor que en el
#asimétrico