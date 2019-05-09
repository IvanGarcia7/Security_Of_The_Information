from Crypto.Hash import SHA3_256


"""
En el caso de que se quiera generar el archivo automáticamente:

documento = "ejercicio1c.docx"
abredocumento = open(documento,"wb")
texto = "Ivan\n Garcia Aguilar"
texto = texto.encode("UTF-8")
abredocumento.write(texto)
abredocumento.close()

"""


documento = 'ejercicio1c.docx'
leedocumento = open(documento,"rb")
codigohash = SHA3_256.new()

#LEO 4 KB
datosleidos = leedocumento.read(4096)

while datosleidos != b'':
    codigohash.update(datosleidos)
    datosleidos = leedocumento.read(4096)

leedocumento.close()
print("El hash SHA3_256 de dicho fichero es:")
print(codigohash.hexdigest())



