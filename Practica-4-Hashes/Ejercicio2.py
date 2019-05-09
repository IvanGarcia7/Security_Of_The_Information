from Crypto.Hash import SHA3_512, HMAC



documento = 'ejercicio1ab.txt'
leedocumento = open(documento,"r")
texto = leedocumento.read()
leedocumento.close()

clave = b'S3cr3tK3y'

codigohash = HMAC.new(clave,digestmod=SHA3_512)
codigohash.update(texto.encode("UTF-8"))

print(codigohash.hexdigest())

firma = codigohash.digest()
try:
    codigohash.verify(firma)
    print("La firma es válida")
except (ValueError,TypeError):
    print("La firma no es válida")



""" A la hora de ejecutar dicho programa, basándome en el creado en el apartado 1b, arroja el siguiente error: ValueError: Hash type incompatible to HMAC
Tipo de HASH incompatible con MAC. Buscando en la documentación, he encontrado que dicho error puesto que no todos los tipos de hash tienen bloques, por ello, HMAC se podrá ejecutar 
con todos los tipos que posean bloques como son : SHA224, SHA256, SHA384, SHA512, SHA512/224, SHA512/256, SHA1, MD2, MD5, RIPEMD160...
Y no se podrá utilizar SHA3-224, SHA3-256, SHA3-384, SHA3-512 por lo comentado anteriormente.
BLAKE2s, BLAKE2b, SHAKE128, SHAKE256, keccak  tampoco se podrán utilizar porque no posee el atributo digest_size

Las variantes del tipo SHA3 o keccak son resistentes a los ataques de extensión de longitud
"""