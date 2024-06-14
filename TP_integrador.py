def obtener_destino(cp):
    longitud = len(cp)
    if longitud == 4:
        return "Bolivia", None
    elif longitud == 5:
        if cp[0] == '1':
            return "Uruguay", True
        else:
            return "Uruguay", False
    elif longitud == 9 and "-" in cp[5]:
        return "Brazil", None
    elif longitud == 8:
        return "Argentina", None
    elif longitud == 7:
        return "Chile", None
    elif longitud == 6:
        return "Paraguay", None
    else:
        return "Otro", None

def obtener_provincia(cp):
    provincias = {
        'a': "Salta", 'b': "Buenos Aires", 'c': "CABA", 'd': "San Luis",
        'e': "Entre Ríos", 'f': "La Rioja", 'g': "Santiago del Estero",
        'h': "Chaco", 'j': "San Juan", 'k': "Catamarca", 'l': "La Pampa",
        'm': "Mendoza", 'n': "Misiones", 'p': "Formosa", 'q': "Neuquén",
        'r': "Río Negro", 's': "Santa Fe", 't': "Tucumán", 'u': "Chubut",
        'v': "Tierra del Fuego, Antártida e Islas del Atlántico Sur", 'w': "Corrientes",
        'x': "Córdoba", 'y': "Jujuy", 'z': "Santa Cruz"
    }
    return provincias.get(cp[0], "Error en la provincia")

def calcular_inicial_tipo(tipo):
    tipos_envio = {
        0: 1100, 1: 1800, 2: 2450, 3: 8300, 4: 10900, 5: 14300, 6: 17900
    }
    return tipos_envio.get(tipo, 0)

def calcular_inicialf(destino, inicial_tipo, cp, is_montevideo):
    if destino in ["Bolivia", "Paraguay"]:
        return inicial_tipo * 1.2
    elif destino == "Argentina":
        return inicial_tipo
    elif destino == "Uruguay":
        return inicial_tipo * (1.2 if is_montevideo else 1.25)
    elif destino == "Chile":
        return inicial_tipo * 1.25
    elif destino == "Brazil":
        if cp[0] in ['8', '9']:
            return inicial_tipo * 1.2
        elif cp[0] in ['0', '1', '2']:
            return inicial_tipo * 1.25
        elif cp[0] in ['4', '5', '6', '7']:
            return inicial_tipo * 1.3
        else:
            return inicial_tipo * 1.5
    else:
        return inicial_tipo * 1.5

def calcular_finalf(inicialf, pago):
    if pago == 1:
        return inicialf * 0.9
    elif pago == 2:
        return inicialf
    else:
        raise ValueError("Ingrese una opción correcta de pago")

def main():
    cp = input("Ingrese el código postal del lugar de destino: ")
    direccion = input("Dirección del lugar de destino: ")
    tipo = int(input("Tipo de envío (id entre 0 y 6): "))
    pago = int(input("Forma de pago (1: efectivo - 2: tarjeta): "))

    destino, is_montevideo = obtener_destino(cp)
    provincia = obtener_provincia(cp) if destino == "Argentina" else "No aplica"
    inicial_tipo = calcular_inicial_tipo(tipo)
    inicialf = calcular_inicialf(destino, inicial_tipo, cp, is_montevideo)
    finalf = calcular_finalf(inicialf, pago)

    inicial = int(inicialf)
    final = int(finalf)

    print("País de destino del envío:", destino)
    print("Provincia destino:", provincia)
    print("Importe inicial a pagar:", inicial)
    print("Importe final a pagar:", final)

if __name__ == "__main__":
    main()
