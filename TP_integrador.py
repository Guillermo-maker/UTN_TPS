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


def obtener_pais(cp):
    for formato, pais in mapa_paises.items():
        if len(cp) == len(formato) and all(
            (c.isdigit() if f == "N" else c.isalpha()) for c, f in zip(cp, formato)
        ):
            return pais
    return "Otros"


def obtener_provincia(cp):
    if cp[0] in mapa_provincias:
        return mapa_provincias[cp[0]]
    return "No aplica"


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


def main():
    # Ejemplo de valores de entrada
    codigo_postal = "C1000ABC"
    direccion = "Calle Falsa 123"
    tipo_envio = 1
    metodo_pago = 1

    pais_destino = obtener_pais(codigo_postal)
    provincia_destino = (
        obtener_provincia(codigo_postal) if pais_destino == "Argentina" else "No aplica"
    )
    importe_inicial = calcular_importe_inicial(tipo_envio, codigo_postal, pais_destino)
    importe_final = calcular_importe_final(importe_inicial, metodo_pago)

    print("País de destino del envío:", pais_destino)
    print("Provincia destino:", provincia_destino)
    print("Importe inicial a pagar:", importe_inicial)
    print("Importe final a pagar:", importe_final)


# Ejecutar el programa
if __name__ == "__main__":
    main()

# Parte 2


def procesar_envios():
    # Leer el archivo
    with open("envios25.txt", "r") as file:
        lines = file.readlines()

    # Leer la primera línea completa y verificar si contiene "HC" o "SC"
    timestamp_line = lines[0].strip()
    if "HC" in timestamp_line:
        control = "HC"
    elif "SC" in timestamp_line:
        control = "SC"

    # Inicializar variables para estadísticas
    cedvalid = 0
    cedinvalid = 0
    imp_acu_total = 0
    ccs = 0
    ccc = 0
    cce = 0
    tipos_carta = [0] * 7  # Contadores para cada tipo de envío
    primer_cp = None
    cant_primer_cp = 0
    menimp = float("inf")
    mencp = ""
    cant_ext = 0
    montos_buenos_aires = []

    # Procesar cada línea de datos
    for line in lines[1:]:
        cp = line[:9].strip()
        address = line[9:29].strip()
        delivery_type = int(line[29])
        payment_method = int(line[30])

        # Validar dirección (solo si el control es HC)
        if control == "HC":
            valid_address = True
            if any(
                c.isupper() and address[i + 1].isupper()
                for i, c in enumerate(address[:-1])
            ):
                valid_address = False
            if not any(c.isdigit() for c in address):
                valid_address = False

            if valid_address:
                cedvalid += 1
            else:
                cedinvalid += 1
        if control == "SC":
            cedvalid += 1

        # Calcular monto inicial y final
        pais = obtener_pais(cp)
        inicial = calcular_importe_inicial(delivery_type, cp, pais)
        final = calcular_importe_final(inicial, payment_method)
        imp_acu_total += final

        # Contar los tipos de envío
        tipos_carta[delivery_type] += 1
        if delivery_type in [0, 1, 2]:
            ccs += 1
        elif delivery_type in [3, 4]:
            ccc += 1
        elif delivery_type in [5, 6]:
            cce += 1

        # Primer CP y su frecuencia
        if primer_cp is None:
            primer_cp = cp
            cant_primer_cp = 1
        elif primer_cp == cp:
            cant_primer_cp += 1

        # Envíos a Brasil
        if pais == "Brasil" and final < menimp:
            menimp = final
            mencp = cp

        # Contar envíos internacionales
        if pais != "Argentina":
            cant_ext += 1

        # Acumular montos para Buenos Aires
        if cp.startswith("B"):
            montos_buenos_aires.append(final)

        # Debugging: Imprimir el estado actual de las variables
        print(f"Procesado CP: {cp}, País: {pais}, Inicial: {inicial}, Final: {final}")
        print(
            f"cedvalid: {cedvalid}, cedinvalid: {cedinvalid}, imp_acu_total: {imp_acu_total}"
        )
        print(f"ccs: {ccs}, ccc: {ccc}, cce: {cce}")
        print(f"primer_cp: {primer_cp}, cant_primer_cp: {cant_primer_cp}")
        print(f"menimp: {menimp}, mencp: {mencp}")
        print(f"cant_ext: {cant_ext}, montos_buenos_aires: {montos_buenos_aires}")

    # Estadísticas adicionales
    tipo_mayor = tipos_carta.index(max(tipos_carta))
    total_envios = sum(tipos_carta)
    porc = (cant_ext / total_envios) * 100 if total_envios else 0
    prom = (
        sum(montos_buenos_aires) / len(montos_buenos_aires)
        if montos_buenos_aires
        else 0
    )

    # Imprimir resultados
    print(" (r1) - Tipo de control de direcciones:", control)
    print(" (r2) - Cantidad de envíos con dirección válida:", cedvalid)
    print(" (r3) - Cantidad de envíos con dirección no válida:", cedinvalid)
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


# Ejecutar el bucle while
while True:
    procesar_envios()
    break  # Aquí puedes cambiar la condición para detener el bucle cuando sea necesario
