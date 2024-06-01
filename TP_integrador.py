# Mapas de códigos postales a países y provincias
mapa_paises = {
    'LNNNNLLL': 'Argentina',
    'NNNN': 'Bolivia',
    'NNNNN-NNN': 'Brasil',
    'NNNNNNN': 'Chile',
    'NNNNNN': 'Paraguay',
    'NNNNN': 'Uruguay'
}

# Mapas de letras de provincias argentinas (ISO 3166-2:AR)
mapa_provincias = {
    'A': 'Salta', 'B': 'Buenos Aires', 'C': 'Capital Federal', 'D': 'San Luis',
    'E': 'Entre Ríos', 'F': 'La Rioja', 'G': 'Santiago del Estero', 'H': 'Chaco',
    'J': 'San Juan', 'K': 'Catamarca', 'L': 'La Pampa', 'M': 'Mendoza',
    'N': 'Misiones', 'P': 'Formosa', 'Q': 'Neuquén', 'R': 'Río Negro',
    'S': 'Santa Fe', 'T': 'Tucumán', 'U': 'Chubut', 'V': 'Tierra del Fuego',
    'W': 'Corrientes', 'X': 'Córdoba', 'Y': 'Jujuy', 'Z': 'Santa Cruz'
}

def obtener_pais(cp):
    for formato, pais in mapa_paises.items():
        if len(cp) == len(formato) and all(
            (c.isdigit() if f == 'N' else c.isalpha()) for c, f in zip(cp, formato)
        ):
            return pais
    return 'Otros'

def obtener_provincia(cp):
    if cp[0] in mapa_provincias:
        return mapa_provincias[cp[0]]
    return 'No aplica'

# Diccionario de precios por tipo de envío y peso
precios_nacionales = {
    0: 1100,
    1: 1800,
    2: 2450,
    3: 8300,
    4: 10900,
    5: 14300,
    6: 17900
}

# Incrementos de precio para envíos internacionales
incrementos_internacionales = {
    'Bolivia': 0.20,
    'Paraguay': 0.20,
    'Uruguay_Montevideo': 0.20,
    'Chile': 0.25,
    'Uruguay': 0.25,
    'Brasil_0_3': 0.25,
    'Brasil_4_7': 0.30,
    'Brasil_8_9': 0.20,
    'Otros': 0.50
}

def calcular_importe_inicial(tipo, cp, pais):
    base = precios_nacionales[tipo]
    if pais == 'Argentina':
        return base
    incremento = 0
    if pais == 'Brasil':
        region = int(cp[0])
        if region in range(0, 4):
            incremento = incrementos_internacionales['Brasil_0_3']
        elif region in range(4, 8):
            incremento = incrementos_internacionales['Brasil_4_7']
        else:
            incremento = incrementos_internacionales['Brasil_8_9']
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






