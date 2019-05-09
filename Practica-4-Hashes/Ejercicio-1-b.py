from Crypto.Hash import SHA512, HMAC



documento = 'ejercicio1ab.txt'
leedocumento = open(documento,"r")
texto = leedocumento.read()
leedocumento.close()

clave = b'S3cr3tK3y'

codigohash = HMAC.new(clave,digestmod=SHA512)
codigohash.update(texto.encode("UTF-8"))

print("El HMAC-SHA512 de dicho fichero es:")
print(codigohash.hexdigest())

firma = codigohash.digest()
try:
    codigohash.verify(firma)
    print("La firma es válida")
except (ValueError,TypeError):
    print("La firma no es válida")


