from Crypto.Cipher import PKCS1_OAEP, DES, AES
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256, HMAC
from Crypto.Signature import pss
from Crypto.Util.Padding import pad,unpad
from Crypto.Random import get_random_bytes
import base64
import json
from socket_class import SOCKET_SIMPLE_TCP

# Parametros
key_a_t = b''
key_b_t = b'FEDCBA9876543210'
BLOCK_SIZE_AES = 16





"""CAPTURO EL MENSAJE EN EL DISCO DURO"""
archivo = "mensaje.docx"
escribearchivo = open(archivo,"rb")
mensajecapturado = escribearchivo.read()
escribearchivo.close()


#Ahora que tengo el mensaje como conozco la clave de b con el servidor descifro el mensaje
msg_b_t = bytearray.fromhex(mensajecapturado.decode("UTF-8"))

# B descifra los datos a través de la clave KBT, guarda la clave KAB y la identidad
# de Alicia y crea un valor random denominado Rb 

uncipher_b_t = AES.new(key_b_t, AES.MODE_ECB)
json_b_t = unpad(uncipher_b_t.decrypt(msg_b_t), BLOCK_SIZE_AES).decode("UTF-8", "ignore")
msg_a_b = json.loads(json_b_t)
a_k_ab, b_alice = msg_a_b
t_k_ab = bytearray.fromhex(a_k_ab)
key_a_t=t_k_ab






#####################################################################
# COMPLETAR: CONTACTAR CON BOB, SEGUIR EL PROTOCOLO NEEDHAM-SCHROEDER
#####################################################################

# Crea el socket servidor y escucha
socket = SOCKET_SIMPLE_TCP('127.0.0.1', 5556)
socket.conectar()


# A envia a B el mensaje recibido por parte del servidor dirigido a B
# A->B: EBT(KAB,ALICE)
socket.enviar(mensajecapturado)

# B genera el valor aleatorio y se lo envía a A usando la clave AB (challengee-response)
#B->A: EAB(RB)
mensaje = socket.recibir()
decipher_b_a = AES.new(t_k_ab, AES.MODE_ECB)
json_b_a = unpad(decipher_b_a.decrypt(mensaje),BLOCK_SIZE_AES).decode("UTF-8")

print("T->A: " + json_b_a)

aleatorio_b = json.loads(json_b_a)[0]
random_b_send = aleatorio_b-1

#A responde a B con el valor aleatorio menos 1
#A->B: EAB(RB-1)
msg_a_b = []
msg_a_b.append(random_b_send)
json_a_b = json.dumps(msg_a_b)

print("A->B: " + json_a_b)

mensaje = decipher_b_a.encrypt(pad(json_a_b.encode("UTF-8"),BLOCK_SIZE_AES))
socket.enviar(mensaje)

#A lee la identidad recibida por B
#B->A: EAB("Bob")

mensaje = socket.recibir()
decipher_b_a = AES.new(t_k_ab, AES.MODE_ECB)
json_b_a = unpad(decipher_b_a.decrypt(mensaje),BLOCK_SIZE_AES).decode("UTF-8")

print("B->A: " + json_b_a)

random_b = json.loads(json_b_a)[0]

#A le envía a B su identidad
#A->B: EAB("Mallory")

msg_a_b = []
msg_a_b.append("Mallory")
json_a_b = json.dumps(msg_a_b)

print("A->B: " + json_a_b)

mensaje = decipher_b_a.encrypt(pad(json_a_b.encode("UTF-8"),BLOCK_SIZE_AES))
socket.enviar(mensaje)