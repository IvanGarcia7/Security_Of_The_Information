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
key_a_t = b'0123456789ABCDEF'
BLOCK_SIZE_AES = 16

# Abre una conexion a T
socket = SOCKET_SIMPLE_TCP('127.0.0.1', 5555)
socket.conectar()

# A: Crear campos
a_alice = "Alice"
a_bob = "Bob"
a_random = get_random_bytes(8)

# A: msg_a_t = Alice, Bob, Ra
msg_a_t = []
msg_a_t.append("Alice")
msg_a_t.append("Bob")
msg_a_t.append(a_random.hex())
json_a_t = json.dumps(msg_a_t)

# A->T: msg_a_t
print("A->T: " + json_a_t)
socket.enviar(json_a_t.encode("utf-8"))

# T->A: E_AT(Ra, Bob, K_AB, E_BT(K_AB, Alice))
# A: Descifrar msg_t_a
datos = socket.recibir()
decipher_aes_a_t = AES.new(key_a_t, AES.MODE_ECB)
json_t_a = unpad(decipher_aes_a_t.decrypt(datos), BLOCK_SIZE_AES).decode("utf-8")
print("T->A (Clear): " + json_t_a)
msg_t_a = json.loads(json_t_a)

# A: Comprobar campos de msg_t_a
t_random, t_bob, t_k_ab, t_bt = msg_t_a
t_random = bytearray.fromhex(t_random)
t_k_ab = bytearray.fromhex(t_k_ab)
if (a_random != t_random):
    print("ERROR: Nonce Equivocado")
    socket.cerrar()
    exit()
if (a_bob != t_bob):
    print("ERROR: Receptor incorrecto")
    socket.cerrar()
    exit()

# Hemos terminado con la conexion con T, podemos cerrar el socket
socket.cerrar()

#####################################################################
# COMPLETAR: CONTACTAR CON BOB, SEGUIR EL PROTOCOLO NEEDHAM-SCHROEDER
#####################################################################

#Establezo la conexión con bob
socket = SOCKET_SIMPLE_TCP('127.0.0.1', 5556)
socket.conectar()

# A envia a B el mensaje recibido por parte del servidor dirigido a B
# A->B: EBT(KAB,ALICE)
print("A->B: " + t_bt)
socket.enviar(t_bt.encode("UTF-8"))


# B genera el valor aleatorio y se lo envía a A usando la clave AB (challengee-response)
#B->A: EAB(RB)
mensaje = socket.recibir()
decipher_b_a = AES.new(t_k_ab, AES.MODE_ECB)
json_b_a = unpad(decipher_b_a.decrypt(mensaje),BLOCK_SIZE_AES).decode("UTF-8")

print("T->A: " + json_b_a)

aleatorio_b = json.loads(json_b_a)[0]
random_b_envia = aleatorio_b-1


#A responde a B con el valor aleatorio menos 1
#A->B: EAB(RB-1)
msg_a_b = []
msg_a_b.append(random_b_envia)
json_a_b = json.dumps(msg_a_b)

print("A->B: " + json_a_b)

mensaje = decipher_b_a.encrypt(pad(json_a_b.encode("UTF-8"),BLOCK_SIZE_AES))
socket.enviar(mensaje)

#Intercambio seguro de nombres

#A lee la identidad recibida por B
#B->A: EAB("Bob")
mensaje = socket.recibir()
decipher_b_a = AES.new(t_k_ab, AES.MODE_ECB)
json_b_a = unpad(decipher_b_a.decrypt(mensaje),BLOCK_SIZE_AES).decode("UTF-8")

print("B->A: " + json_b_a)

aleatorio_b = json.loads(json_b_a)[0]


#A le envía a B su identidad
#A->B: EAB("Alice")
msg_a_b = []
msg_a_b.append("ALICIA")
json_a_b = json.dumps(msg_a_b)

print("A->B: " + json_a_b)

mensaje = decipher_b_a.encrypt(pad(json_a_b.encode("UTF-8"),BLOCK_SIZE_AES))
socket.enviar(mensaje)

