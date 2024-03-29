from socket_class import SOCKET_SIMPLE_TCP
from rsa_class import RSA_OBJECT
from aes_class import AES_CIPHER
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import base64
import json

# Recibe la informacion del cliente
###################################
# Crea el socket en 5555
print("Creando socket y escuchando...")
socket = SOCKET_SIMPLE_TCP('127.0.0.1', 5555)
socket.escuchar()

# Recibe los datos y cierra el socket
datos = socket.recibir()
json_vendedor = datos.decode("utf-8" ,"ignore")
socket.cerrar()

# Decodifica los datos
msg_cliente = json.loads(json_vendedor)
json_banco_cifrado_hex, IV_banco_hex, digital_envelope_hex, PIMD_hex, OI_vendedor, firma_dual_hex, pub_usuario_hex = msg_cliente

#####################################################
# A REALIZAR POR EL ALUMNO
#
# Comprobar que la informacion recibida por parte 
# del cliente es integra, considerando en este caso
# la firma dual computada por dicho cliente
######################################################


#Calculo la variable firma dual del cliente pasandola de hexadecimal a binario
firma_dual_cliente = bytearray.fromhex(firma_dual_hex)


pub_usuario = bytearray.fromhex(pub_usuario_hex)
RSA_Usuario = RSA_OBJECT()
RSA_Usuario.set_PublicKeyPEM(pub_usuario)



OIMD = SHA256.new(OI_vendedor.encode("UTF-8")).digest()

PIMD = bytearray.fromhex(PIMD_hex)

Calculo_Hash = OIMD+PIMD

#Calculo el HASH
OIPI = SHA256.new(Calculo_Hash).digest()



######################################################

if not RSA_Usuario.verify(OIPI,firma_dual_cliente): # a terminar también por el alumno ... 
    print("firma dual invalida")
    exit()





# Prepara el genero para la venta :-)
print("VENDEDOR: " + OI_vendedor)

# Enviar informacion al banco
#############################

# Los campos son los siguientes:
# - Mensaje cifrado para el banco
# - IV usado en el mensaje cifrado para el banco
# - "digital envelope" (clave del mensaje cifrado para el banco, cifrado con kPubBanco)
msg_banco = []
msg_banco.append(json_banco_cifrado_hex)
msg_banco.append(IV_banco_hex)
msg_banco.append(digital_envelope_hex)
msg_banco.append(pub_usuario_hex)

json_banco = json.dumps(msg_banco)

# Abre una conexion al banco
socketBanco = SOCKET_SIMPLE_TCP('127.0.0.1', 5556)
socketBanco.conectar()

# Envia los datos
print("Vendedor -> Banco: mensaje")
socketBanco.enviar(json_banco.encode("utf-8"))

# Cierra el canal
socketBanco.cerrar()

print("Vendedor finalizado correctamente")
