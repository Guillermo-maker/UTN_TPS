import re

# Diccionario de precios por tipo de envío y peso
precios_nacionales = {0: 1100, 1: 1800, 2: 2450, 3: 8300, 4: 10900, 5: 14300, 6: 17900}

# Incrementos de precio para envíos internacionales
incrementos_internacionales = {
    "Bolivia": 0.20,
    "Paraguay": 0.20,
    "Uruguay_Montevideo": 0.20,
    "Chile": 0.25,
    "Uruguay": 0.25,
    "Brasil_0_3": 0.25,
    "Brasil_4_7": 0.30,
    "Brasil_8_9": 0.20,
    "Otros": 0.50,
}

# Mapas de códigos postales a países y provincias
mapa_paises = {
    "LNNNNLLL": "Argentina",
    "NNNN": "Bolivia",
    "NNNNN-NNN": "Brasil",
    "NNNNNNN": "Chile",
    "NNNNNN": "Paraguay",
    "NNNNN": "Uruguay",
}

# Mapas de letras de provincias argentinas (ISO 3166-2:AR)
mapa_provincias = {
    "A": "Salta",
    "B": "Buenos Aires",
    "C": "Capital Federal",
    "D": "San Luis",
    "E": "Entre Ríos",
    "F": "La Rioja",
    "G": "Santiago del Estero",
    "H": "Chaco",
    "J": "San Juan",
    "K": "Catamarca",
    "L": "La Pampa",
    "M": "Mendoza",
    "N": "Misiones",
    "P": "Formosa",
    "Q": "Neuquén",
    "R": "Río Negro",
    "S": "Santa Fe",
    "T": "Tucumán",
    "U": "Chubut",
    "V": "Tierra del Fuego",
    "W": "Corrientes",
    "X": "Córdoba",
    "Y": "Jujuy",
    "Z": "Santa Cruz",
}


def validar_direccion_hard_control(direccion):
    # Reemplazar punto al final por espacio en blanco
    direccion = direccion.rstrip(".") + " "

    # Validación específica para Hard Control
    if not re.search(r"\d", direccion):  # Debe contener al menos un dígito
        return False
    if re.search(r"[^a-zA-Z0-9 ]", direccion):  # Solo letras, dígitos y espacio
        return False
    if re.search(r"[A-Z]{2}", direccion):  # No puede haber dos mayúsculas seguidas
        return False
    if not re.search(
        r"\b\d+\b", direccion
    ):  # Debe haber al menos una palabra compuesta solo por dígitos
        return False
    return True


def obtener_pais(cp):
    for formato, pais in mapa_paises.items():
        if len(cp) == len(formato) and all(
            (c.isdigit() if f == "N" else c.isalpha())
            for c, f in zip(cp.replace("-", ""), formato.replace("-", ""))
        ):
            return pais
    return "Otros"


def obtener_provincia(cp):
    if cp[0] in mapa_provincias:
        return mapa_provincias[cp[0]]
    return "No aplica"


def calcular_importe_inicial(tipo, cp, pais):
    base = precios_nacionales[tipo]
    if pais == "Argentina":
        return base
    incremento = 0
    if pais == "Brasil":
        region = int(cp[0])
        if region in range(0, 4):
            incremento = incrementos_internacionales["Brasil_0_3"]
        elif region in range(4, 8):
            incremento = incrementos_internacionales["Brasil_4_7"]
        else:
            incremento = incrementos_internacionales["Brasil_8_9"]
    elif pais in incrementos_internacionales:
        incremento = incrementos_internacionales[pais]
    else:
        incremento = incrementos_internacionales["Otros"]
    return int(base * (1 + incremento))


def calcular_importe_final(inicial, pago):
    if pago == 1:
        return int(inicial * 0.90)  # 10% de descuento
    return inicial


# Contadores para validos e invalidos
cedvalid = 0
cedinvalid = 0

# Lectura del archivo envios25.txt
with open("envios25.txt", "r") as archivo:
    lineas = archivo.readlines()

# Procesamiento de timestamp (en este caso, asumiendo solo la primera línea como timestamp)
timestamp = lineas[0].strip()
control = ""

if "HC" in timestamp:
    control = "Hard Control"
else:
    "Soft Control"

imp_acu_total = 0
tipos_carta = [0] * 7
ccs = 0
ccc = 0
cce = 0
cant_primer_cp = 0
primer_cp = None

menimp = float("inf")
mencp = ""

cant_ext = 0
montos_buenos_aires = []

# Iterar sobre las líneas de envíos
for linea in lineas[1:]:
    cp = linea[:9].strip()  # Código postal, primeros 9 caracteres
    direccion = linea[9:29].strip()  # Dirección, siguientes 20 caracteres
    tipo_envio = int(linea[29])  # Tipo de envio especificado en el caracter 29
    tipo_pago = int(linea[30])  # Tipo de pago especificado en el caracter 30
    pais = obtener_pais(cp)
    inicial = calcular_importe_inicial(tipo_envio, cp, pais)
    final = calcular_importe_final(inicial, tipo_pago)
    tipos_carta[tipo_envio] += 1
    print("Pais: ", pais, " CP: ", cp, " Importe a pagar: ", final)

    # Acumular montos para Buenos Aires
    if cp.startswith("B"):
        montos_buenos_aires.append(final)
        prom = sum(montos_buenos_aires) / len(montos_buenos_aires)

    # Validar dirección según el tipo de control
    if control == "Hard Control":
        es_valida = validar_direccion_hard_control(direccion)
    else:
        es_valida = True
    if es_valida:
        cedvalid += 1
    else:
        cedinvalid += 1

    # Contar los tipos de envío
    if es_valida and tipo_envio in [0, 1, 2]:
        ccs += 1
    elif es_valida and tipo_envio in [3, 4]:
        ccc += 1
    elif es_valida and tipo_envio in [5, 6]:
        cce += 1

    # Calcular monto inicial y final(NO ANDA Y NO SE PORQUE AAAAAAAAAAAAAAAAAAAA)
    if es_valida:
        imp_acu_total += final

    # Primer codigo postal del archivo y cuantas veces aparece
    if primer_cp is None and es_valida:
        primer_cp = cp
        cant_primer_cp = 1
    elif primer_cp == cp and es_valida:
        cant_primer_cp += 1

    tipo_mayor = ""
    mayor_envio = tipos_carta.index(max(tipos_carta))
    if mayor_envio in [0, 1, 2]:
        tipo_mayor = "Carta simple"
    elif mayor_envio in [3, 4]:
        tipo_mayor = "Carta certificada"
    elif mayor_envio in [5, 6]:
        tipo_mayor = "Carta expresa"

    # Contar envíos internacionales
    if pais != "Argentina" and es_valida:
        cant_ext += 1
    total_envios = sum(tipos_carta)
    porc = (cant_ext / total_envios) * 100

    # Para los filtros de brasil
    if pais == "Brasil" and es_valida and final < menimp:
        menimp = final
        mencp = cp


# Mostrar resultados
print(f" (r1) - Tipo de control de direcciones:", control)
print(" (r2) - Cantidad de envios con direccion valida:", cedvalid)
print(" (r3) - Cantidad de envios con direccion no valida:", cedinvalid)
print(" (r4) - Total acumulado de importes finales:", imp_acu_total)
print(" (r5) - Cantidad de cartas simples:", ccs)
print(" (r6) - Cantidad de cartas certificadas:", ccc)
print(" (r7) - Cantidad de cartas expresas:", cce)
print(" (r8) - Tipo de carta con mayor cantidad de envíos:", tipo_mayor)
print(" (r9) - Código postal del primer envío del archivo:", primer_cp)
print("(r10) - Cantidad de veces que entró ese primero:", cant_primer_cp)
print("(r11) - Importe menor pagado por envíos a Brasil:", menimp)
print("(r12) - Código postal del envío a Brasil con importe menor:", mencp)
print("(r13) - Porcentaje de envíos al exterior sobre el total:", porc)
print("(r14) - Importe final promedio de los envíos Buenos Aires:", prom)
