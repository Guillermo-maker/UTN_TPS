cp = input ("Ingrese el código postal del lugar de destino: ").lower()
direccion = input("Dirección del lugar de destino: ")
tipo = int(input("Tipo de envío (id entre 0 y 6): "))
pago = int(input("Forma de pago (1: efectivo - 2: tarjeta): "))
is_montevideo = None
destino = ""
provincia = ""
final=""
inicial = ""

if len(cp) == 4:
   destino == "Bolivia"
elif len(cp) == 5:
    destino= "Uruguay"
    if '1' in cp[0]:
        is_montevideo = True
    else :
        is_montevideo = False
elif len(cp) == 9:
    destino= "Brazil"
elif len(cp) == 8:
    destino= "Argentina"
elif len(cp) == 7:
    destino= "Chile"
elif len(cp) == 6:
    destino= "Paraguay"
else:
    print("Verificar el codigo postal")

if destino == "Argentina": 
    if 'a' in cp[0]:
        provincia = "Salta"
    elif "b" in cp[0] and "a" in cp[1]: 
        provincia = "buenos Aires"
    elif  "c" in cp[0]:
        provincia = "CABA"
    elif 'd' in cp[0]:
        provincia  = "San Luis"
    elif "e" in cp[0]:
        provincia = "Entre Ríos"
    elif  "f" in cp[0]:
        provincia = "La Rioja"
    elif 'g' in cp[0]:
        provincia  = "Santiago del Estero"
    elif 'h' in cp[0]:
        provincia  = "Chaco"
    elif  "j" in cp[0]:
        provincia = "San Juan"
    elif 'k' in cp[0]:
        provincia  = "Catamarca"
    elif 'l' in cp[0]:
        provincia  = "La Pampa"
    elif  "m" in cp[0]:
        provincia = "Mendoza"
    elif 'p' in cp[0]:
        provincia  = "Formosa"
    elif 'q' in cp[0]:
        provincia  = "Neuquén"
    elif  "m" in cp[0]:
        provincia = "Mendoza"
    elif  "n" in cp[0]:
        provincia = "Misiones"
    elif 'p' in cp[0]:
        provincia  = "Formosa"
    elif 'q' in cp[0]:
        provincia  = "Neuquén"
    elif  "r" in cp[0]:
        provincia = "Río Negro"
    elif 's' in cp[0]:
        provincia  = "Santa Fe"
    elif 't' in cp[0]:
        provincia  = "Tucumán"
    elif  "u" in cp[0]:
        provincia = "Chubut"
    elif 'v' in cp[0]:
        provincia  = "Tierra del Fuego, Antártida e Islas del Atlántico Sur"
    elif 'w' in cp[0]:
        provincia  = "Corrientes"
    elif 'x' in cp[0]:
        provincia = "cordoba"
    elif 'y' in cp[0]:
        provincia = "Jujuy"
    elif 'z' in cp[0]:
        provincia = "Santa Cruz"
    else:
        print("Error en la provincia")

# Tabla 2 - Tipo envio 

if tipo == "0":
    incial = 1100
elif tipo == "1":
     incial = 1800
elif  tipo == "2":
    incial = 2450
elif tipo  == "3":
    incial = 8300
elif tipo == "4": 
    inical = 10900
elif  tipo == "5":
    incial = 14300
elif tipo  == "6":
    inicial =17900
 
 #Tabla 3

if destino == "Bolivia" or  destino == "Paraguay":
    final = inicial + (inicial * 0.2)
elif  destino == "Uruguay" and is_montevideo == True:
    final = inicial + (inicial *0.2)
elif destino  == "Chile":
    final=inicial+ (inicial*0.25)
elif destino == "Uruguay" and is_montevideo == False:
    final=inicial+ (inicial*0.25)
elif destino == "Brazil" and ("8" in cp[0] or "9" in cp[0]):
    final = inicial + (inicial *0.2)
elif destino == "Brazil" and ("0" in cp[0] or"1" in cp[0] or "2" in cp[0]) :
    final = inicial + (inicial *0.25)
elif destino == "Brazil" and ("4" in cp[0] or "5" in cp[0] or "6" in cp[0] or "7" in cp[0]) :
    final = inicial + (inicial *0.3)
else:
    final = inicial + (inicial*0.5)


print("Provincia destino:", provincia)
print("País de destino del envío:", destino)
print("Importe inicial a pagar:", inicial)
print("Importe final a pagar:", final) 






