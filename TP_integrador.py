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
    elif pais == 'Bolivia':
        incremento = incrementos_internacionales['Bolivia']
    elif pais == 'Paraguay':
        incremento = incrementos_internacionales['Paraguay']
    elif pais == 'Uruguay':
        if cp.startswith('11'):
            incremento = incrementos_internacionales['Uruguay_Montevideo']
        else:
            incremento = incrementos_internacionales['Uruguay']
    elif pais == 'Chile':
        incremento = incrementos_internacionales['Chile']
    else:
        incremento = incrementos_internacionales['Otros']
    return int(base * (1 + incremento))

def calcular_importe_final(inicial, pago):
    if pago == 1:
        return int(inicial * 0.90)  # 10% de descuento
    return inicial

def main():
    cp = ""
    direccion = ""
    tipo = ""
    pago = ""

    destino = obtener_pais(cp)
    provincia = obtener_provincia(cp) if destino == 'Argentina' else 'No aplica'
    inicial = calcular_importe_inicial(tipo, cp, destino)
    final = calcular_importe_final(inicial, pago)

    print("País de destino del envío:", destino)
    print("Provincia destino:", provincia)
    print("Importe inicial a pagar:", inicial)
    print("Importe final a pagar:", final)

# Ejecutar el programa
if __name__ == "__main__":
    main()

# Parte 2 

# Leer el archivo
with open('envios25.txt', 'r') as file:
    lines = file.readlines()

# Definir la función para procesar las líneas
def lectura_archivo(lines):
    for line in lines:
        # Procesar cada línea
        print(line.strip())  # Ejemplo: imprimir la línea sin espacios en blanco alrededor

# Llamar a la función con las líneas leídas del archivo
lectura_archivo(lines)


# Leer la primera línea (timestamp)
timestamp_line = lines[0].strip().split()
control_type = timestamp_line[2]

# Inicializar variables para estadísticas
valid_count = 0
invalid_count = 0
total_amount = 0
simple_count = 0
certified_count = 0
express_count = 0
delivery_types_count = [0] * 7  # Contadores para cada tipo de envío
first_cp = None
first_cp_count = 0
min_brazil_amount = float('inf')
min_brazil_cp = ''
international_count = 0
buenos_aires_amounts = []

# Procesar cada línea de datos
for line in lines[1:]:
    cp = line[:9].strip()
    address = line[9:29].strip()
    delivery_type = int(line[29])
    payment_method = int(line[30])

    # Validar dirección (solo si el control es HC)
    if control_type == 'HC':
        valid_address = True
        if not address.replace(' ', '').isalnum():
            valid_address = False
        if any(c.isupper() and address[i+1].isupper() for i, c in enumerate(address[:-1])):
            valid_address = False
        if not any(c.isdigit() for c in address):
            valid_address = False

        if valid_address:
            valid_count += 1
        else:
            invalid_count += 1
            continue  # Saltar a la siguiente línea si la dirección es inválida

    if control_type == 'SC':


    # Calcular monto inicial
    if cp.startswith('A'):
        provincia = 'Buenos Aires'
    else:
        provincia = obtener_provincia(cp)

    # Determinar país del destino
    if len(cp) == 8 and cp[0].isalpha() and cp[1:5].isdigit() and cp[5:].isalpha():
        pais = 'Argentina'
    elif len(cp) == 4 and cp.isdigit():
        pais = 'Bolivia'
    elif len(cp) == 9 and cp[:5].isdigit() and cp[5] == '-' and cp[6:].isdigit():
        pais = 'Brasil'
    elif len(cp) == 7 and cp.isdigit():
        pais = 'Chile'
    elif len(cp) == 6 and cp.isdigit():
        pais = 'Paraguay'
    elif len(cp) == 5 and cp.isdigit():
        pais = 'Uruguay'
    else:
        pais = 'Otros'

    # Calcular el importe inicial
    importe_inicial = precios_nacionales[delivery_type]
    if pais != 'Argentina':
        if pais == 'Bolivia':
            incremento = 1.20
        elif pais == 'Paraguay':
            incremento = 1.20
        elif pais == 'Uruguay' and cp.startswith('11'):
            incremento = 1.20
        elif pais == 'Chile':
            incremento = 1.25
        elif pais == 'Uruguay':
            incremento = 1.25
        elif pais == 'Brasil' and cp[0] in '0123':
            incremento = 1.25
        elif pais == 'Brasil' and cp[0] in '4567':
            incremento = 1.30
        elif pais == 'Brasil':
            incremento = 1.20
        else:
            incremento = 1.50
        importe_inicial = int(importe_inicial * incremento)

    # Calcular el importe final
    if payment_method == 1:
        importe_final = int(importe_inicial * 0.90)
    else:
        importe_final = importe_inicial

    total_amount += importe_final

    # Contar los tipos de envío
    delivery_types_count[delivery_type] += 1
    if delivery_type in [0, 1, 2]:
        simple_count += 1
    elif delivery_type in [3, 4]:
        certified_count += 1
    elif delivery_type in [5, 6]:
        express_count += 1

    # Primer CP y su frecuencia
    if first_cp is None:
        first_cp = cp
        first_cp_count = 1
    elif first_cp == cp:
        first_cp_count += 1

    # Envíos a Brasil
    if pais == 'Brasil' and importe_final < min_brazil_amount:
        min_brazil_amount = importe_final
        min_brazil_cp = cp

    # Contar envíos internacionales
    if pais != 'Argentina':
        international_count += 1

    # Acumular montos para Buenos Aires
    if cp.startswith('B'):
        buenos_aires_amounts.append(importe_final)

# Estadísticas adicionales
most_frequent_type = delivery_types_count.index(max(delivery_types_count))
total_deliveries = sum(delivery_types_count)
international_percentage = (international_count / total_deliveries) * 100 if total_deliveries else 0
average_buenos_aires = sum(buenos_aires_amounts) / len(buenos_aires_amounts) if buenos_aires_amounts else 0

# Imprimir resultados
print(' (r1) - Tipo de control de direcciones:', control)
print(' (r2) - Cantidad de envios con direccion valida:', cedvalid)
print(' (r3) - Cantidad de envios con direccion no valida:', cedinvalid)
print(' (r4) - Total acumulado de importes finales:', imp_acu_total)
print(' (r5) - Cantidad de cartas simples:', ccs)
print(' (r6) - Cantidad de cartas certificadas:', ccc)
print(' (r7) - Cantidad de cartas expresas:', cce)
print(' (r8) - Tipo de carta con mayor cantidad de envios:', tipo_mayor)
print(' (r9) - Codigo postal del primer envio del archivo:', primer_cp)
print('(r10) - Cantidad de veces que entro ese primero:', cant_primer_cp)
print('(r11) - Importe menor pagado por envios a Brasil:', menimp)
print('(r12) - Codigo postal del envio a Brasil con importe menor:', mencp)
print('(r13) - Porcentaje de envios al exterior sobre el total:', porc)
print('(r14) - Importe final promedio de los envios Buenos Aires:', prom)
