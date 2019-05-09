from Crypto.Cipher import PKCS1_OAEP, DES, AES
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256, HMAC
from Crypto.Signature import pss
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes
import base64
import json
from socket_class import SOCKET_SIMPLE_TCP
from random import randint

# Parametros
key_b_t = b'FEDCBA9876543210'
BLOCK_SIZE_AES = 16

# Crea el socket servidor y escucha
print("Creando socket y escuchando...")
socket = SOCKET_SIMPLE_TCP('127.0.0.1', 5556)
socket.escuchar()

# A->B: EBT(KAB,ALICE)
datos = socket.recibir()
msg_b_t = bytearray.fromhex(datos.decode("UTF-8"))


# B descifra los datos a través de la clave KBT, guarda la clave KAB y la identidad
# de Alicia y crea un valor random denominado Rb 


uncipher_b_t = AES.new(key_b_t, AES.MODE_ECB)
json_b_t = unpad(uncipher_b_t.decrypt(msg_b_t), BLOCK_SIZE_AES).decode("UTF-8", "ignore")

print("A->B: " + json_b_t)

mensaje_a_b = json.loads(json_b_t)
a_k_ab, b_alice = mensaje_a_b
a_k_ab = bytearray.fromhex(a_k_ab)

#Creo un número random de 0 a 10 millones por ejemplo
b_aleatorio = randint(0, 10000000)

#Envio a A el valor random generado
#B->A: EAB(RB)

msg_b_a = []
msg_b_a.append(b_aleatorio)

cipher_a_b = AES.new(a_k_ab, AES.MODE_ECB)
json_b_a = json.dumps(msg_b_a)

print("B->A: " + json_b_a)

mensaje = cipher_a_b.encrypt(pad(json_b_a.encode("UTF-8"),BLOCK_SIZE_AES))
socket.enviar(mensaje)

#Recibo de A el valor restado -1
#A->B: EAB(RB-1)

mensaje = socket.recibir()
json_b_a = unpad(cipher_a_b.decrypt(mensaje),BLOCK_SIZE_AES).decode("UTF-8")

print("T->A : " + json_b_a)

random_b = json.loads(json_b_a)[0]

#Realizo la comprobacion
if (b_aleatorio-1 != random_b):
    print("ERROR: El Nonce no es correcto")
    socket.cerrar()
    exit()

#B envia a A su identidad 
#B->A: EAB("Bob")

msg_b_a = []
msg_b_a.append("BOB")

cipher_a_b = AES.new(a_k_ab, AES.MODE_ECB)
json_b_a = json.dumps(msg_b_a)

print("B->A : " + json_b_a)
mensaje = cipher_a_b.encrypt(pad(json_b_a.encode("UTF-8"),BLOCK_SIZE_AES))
socket.enviar(mensaje)

#B recibe la identidad de A
#A->B: EAB("Alice")

mensaje = socket.recibir()
json_b_a = unpad(cipher_a_b.decrypt(mensaje),BLOCK_SIZE_AES).decode("UTF-8")

print("A->B: " + json_b_a)
random_b = json.loads(json_b_a)[0]

# Cerramos el Socket
socket.cerrar()
