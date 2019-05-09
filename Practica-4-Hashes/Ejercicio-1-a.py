from Crypto.Hash import SHA512


"""
En el caso de que se quiera generar el archivo automáticamente:

documento = "ejercicio1ab.txt"
abredocumento = open(documento,"w")
texto = "Ivan\n Garcia Aguilar"
abredocumento.write(texto)
abredocumento.close()

"""


documento = 'ejercicio1ab.txt'
leedocumento = open(documento,"r")
texto = leedocumento.read()
leedocumento.close()

codigohash = SHA512.new(texto.encode("UTF-8"))
print("El hash SHA512 de dicho fichero es:")
print(codigohash.hexdigest())


