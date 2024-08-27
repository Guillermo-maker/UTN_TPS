import re


def obtener_precio_nacional(tipo):
    precios = [1100, 1800, 2450, 8300, 10900, 14300, 17900]
    return precios[tipo] if 0 <= tipo < len(precios) else 0


def obtener_incremento_internacional(pais, cp):
    if pais in ["Bolivia", "Paraguay", "Uruguay_Montevideo"]:
        return 0.20
    elif pais in ["Chile", "Uruguay"]:
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
        return 0.50


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
    provincias = {
        "A": "Salta", "B": "Buenos Aires", "C": "Capital Federal", "D": "San Luis", "E": "Entre Ríos",
        "F": "La Rioja", "G": "Santiago del Estero", "H": "Chaco", "J": "San Juan", "K": "Catamarca",
        "L": "La Pampa", "M": "Mendoza", "N": "Misiones", "P": "Formosa", "Q": "Neuquén",
        "R": "Río Negro", "S": "Santa Fe", "T": "Tucumán", "U": "Chubut", "V": "Tierra del Fuego",
        "W": "Corrientes", "X": "Córdoba", "Y": "Jujuy", "Z": "Santa Cruz"
    }
    return provincias.get(cp[0], "No aplica")


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
    return int(inicial * 0.90) if pago == 1 else inicial


def procesar_envios():
    cedvalid = 0
    cedinvalid = 0

    with open("envios25.txt", "r") as archivo:
        lineas = archivo.readlines()

    timestamp = lineas[0].strip()
    control = "Hard Control" if "HC" in timestamp else "Soft Control"

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

    for linea in lineas[1:]:
        cp = linea[:9].strip()
        direccion = linea[9:29].strip()
        tipo_envio = int(linea[29])
        tipo_pago = int(linea[30])
        pais = obtener_pais(cp)
        inicial = calcular_importe_inicial(tipo_envio, cp, pais)
        final = calcular_importe_final(inicial, tipo_pago)
        tipos_carta[tipo_envio] += 1

        if control == "Hard Control":
            es_valida = validar_direccion_hard_control(direccion)
        else:
            es_valida = True

        if es_valida:
            cedvalid += 1
        else:
            cedinvalid += 1

        if es_valida:
            if tipo_envio in [0, 1, 2]:
                ccs += 1
            elif tipo_envio in [3, 4]:
                ccc += 1
            elif tipo_envio in [5, 6]:
                cce += 1

        if cp.startswith("B") and es_valida and len(cp) == 8 and cp[1:5].isdigit() and cp[5:].isalpha():
            montos_buenos_aires.append(final)
            prom = int(sum(montos_buenos_aires) / len(montos_buenos_aires))

        if es_valida:
            imp_acu_total += final

        if primer_cp is None:
            primer_cp = cp
            cant_primer_cp = 1
        elif primer_cp == cp:
            cant_primer_cp += 1

        if es_valida:
            if pais != "Argentina":
                cant_ext += 1

            if pais == "Brasil" and final < menimp:
                menimp = final
                mencp = cp

    total_envios = sum(tipos_carta)
    porc = int((cant_ext / total_envios) * 100)
    tipo_mayor = ["Carta simple", "Carta certificada", "Carta expresa"][tipos_carta.index(max(tipos_carta)) // 2]

    return {
        "control": control,
        "cedvalid": cedvalid,
        "cedinvalid": cedinvalid,
        "imp_acu_total": imp_acu_total,
        "ccs": ccs,
        "ccc": ccc,
        "cce": cce,
        "tipo_mayor": tipo_mayor,
        "primer_cp": primer_cp,
        "cant_primer_cp": cant_primer_cp,
        "menimp": menimp,
        "mencp": mencp,
        "porc": porc,
        "prom": prom if 'prom' in locals() else 0
    }


def main():
    resultados = procesar_envios()

    print(f" (r1) - Tipo de control de direcciones: {resultados['control']}")
    print(f" (r2) - Cantidad de envios con direccion valida: {resultados['cedvalid']}")
    print(f" (r3) - Cantidad de envios con direccion no valida: {resultados['cedinvalid']}")
    print(f" (r4) - Total acumulado de importes finales: {resultados['imp_acu_total']}")
    print(f" (r5) - Cantidad de cartas simples: {resultados['ccs']}")
    print(f" (r6) - Cantidad de cartas certificadas: {resultados['ccc']}")
    print(f" (r7) - Cantidad de cartas expresas: {resultados['cce']}")
    print(f" (r8) - Tipo de carta con mayor cantidad de envíos: {resultados['tipo_mayor']}")
    print(f" (r9) - Código postal del primer envío del archivo: {resultados['primer_cp']}")
    print(f"(r10) - Cantidad de veces que entró ese primero: {resultados['cant_primer_cp']}")
    print(f"(r11) - Importe menor pagado por envíos a Brasil: {resultados['menimp']}")
    print(f"(r12) - Código postal del envío a Brasil con importe menor: {resultados['mencp']}")
    print(f"(r13) - Porcentaje de envíos al exterior sobre el total: {resultados['porc']}")
    print(f"(r14) - Importe final promedio de los envíos Buenos Aires: {resultados['prom']}")


if __name__ == '__main__':
    main()
