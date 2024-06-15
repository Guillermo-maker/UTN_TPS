import re


def obtener_precio_nacional(tipo):
    if tipo == 0:
        return 1100
    elif tipo == 1:
        return 1800
    elif tipo == 2:
        return 2450
    elif tipo == 3:
        return 8300
    elif tipo == 4:
        return 10900
    elif tipo == 5:
        return 14300
    elif tipo == 6:
        return 17900
    else:
        return 0  # En caso de un tipo de envío no válido


def obtener_incremento_internacional(pais, cp):
    if pais == "Bolivia" or pais == "Paraguay":
        return 0.20
    elif pais == "Uruguay_Montevideo":
        return 0.20
    elif pais == "Chile" or pais == "Uruguay":
        return 0.25
    elif pais == "Brasil":
        region = int(cp[0])
        if region in range(0, 4):
            return 0.25
        elif region in range(4, 8):
            return 0.30
        else:
            return 0.20
    else:
        return 0.50  # Otros países


def validar_direccion_hard_control(direccion):
    direccion = direccion.rstrip(".") + " "
    if not re.search(r"\d", direccion):
        return False
    if re.search(r"[^a-zA-Z0-9 ]", direccion):
        return False
    if re.search(r"[A-Z]{2}", direccion):
        return False
    if not re.search(r"\b\d+\b", direccion):
        return False
    return True


def obtener_provincia(cp):
    if cp[0] == "A":
        return "Salta"
    elif cp[0] == "B":
        return "Buenos Aires"
    elif cp[0] == "C":
        return "Capital Federal"
    elif cp[0] == "D":
        return "San Luis"
    elif cp[0] == "E":
        return "Entre Ríos"
    elif cp[0] == "F":
        return "La Rioja"
    elif cp[0] == "G":
        return "Santiago del Estero"
    elif cp[0] == "H":
        return "Chaco"
    elif cp[0] == "J":
        return "San Juan"
    elif cp[0] == "K":
        return "Catamarca"
    elif cp[0] == "L":
        return "La Pampa"
    elif cp[0] == "M":
        return "Mendoza"
    elif cp[0] == "N":
        return "Misiones"
    elif cp[0] == "P":
        return "Formosa"
    elif cp[0] == "Q":
        return "Neuquén"
    elif cp[0] == "R":
        return "Río Negro"
    elif cp[0] == "S":
        return "Santa Fe"
    elif cp[0] == "T":
        return "Tucumán"
    elif cp[0] == "U":
        return "Chubut"
    elif cp[0] == "V":
        return "Tierra del Fuego"
    elif cp[0] == "W":
        return "Corrientes"
    elif cp[0] == "X":
        return "Córdoba"
    elif cp[0] == "Y":
        return "Jujuy"
    elif cp[0] == "Z":
        return "Santa Cruz"
    else:
        return "No aplica"


def obtener_pais(cp):
    provincia = obtener_provincia(cp)
    if len(cp) == 8 and cp[0].isalpha() and cp[1:5].isdigit() and cp[5:8].isalpha():
        return "Argentina" if provincia != "No aplica" else "Otros"
    elif len(cp) == 4 and cp.isdigit():
        return "Bolivia"
    elif len(cp) == 9 and cp[:5].isdigit() and cp[6:].isdigit() and cp[5] == "-":
        return "Brasil"
    elif len(cp) == 7 and cp.isdigit():
        return "Chile"
    elif len(cp) == 6 and cp.isdigit():
        return "Paraguay"
    elif len(cp) == 5 and cp.isdigit():
        return "Uruguay"
    else:
        return "Otros"


def calcular_importe_inicial(tipo, cp, pais):
    base = obtener_precio_nacional(tipo)
    if pais == "Argentina":
        return base
    incremento = obtener_incremento_internacional(pais, cp)
    return int(base * (1 + incremento))


def calcular_importe_final(inicial, pago):
    if pago == 1:
        return int(inicial * 0.90)  # 10% de descuento
    return inicial


# Contadores para validos e invalidos
cedvalid = 0
cedinvalid = 0

# Lectura del archivo envios500b.txt
with open("envios500b.txt", "r") as archivo:
    lineas = archivo.readlines()

# Procesamiento de timestamp (en este caso, asumiendo solo la primera línea como timestamp)
timestamp = lineas[0].strip()
control = ""

if "HC" in timestamp:
    control = "Hard Control"
else:
    control = "Soft Control"

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

    # Acumular montos para Buenos Aires
    if cp.startswith("B") and es_valida:
        montos_buenos_aires.append(final)
        prom = sum(montos_buenos_aires) / len(montos_buenos_aires)

    # Calcular monto inicial y final
    if es_valida:
        imp_acu_total += final

    # Primer codigo postal del archivo y cuantas veces aparece
    if primer_cp is None:
        primer_cp = cp
        cant_primer_cp = 1
    elif primer_cp == cp:
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
    porc = int((cant_ext / total_envios) * 100)

    # Para los filtros de brasil
    if pais == "Brasil" and final < menimp:
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
