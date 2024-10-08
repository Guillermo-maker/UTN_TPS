import csv
import struct

# Estructura del registro en el archivo binario
FORMATO_BINARIO = "9s20siib"  # CP (9 bytes), Dirección (20 bytes), Tipo Envío (int), Tipo Pago (int), Importe Final (int)
TAMANIO_REGISTRO = struct.calcsize(FORMATO_BINARIO)


# Función para calcular el importe final
def calcular_importe_inicial(tipo, pais, cp):
    precios = [1100, 1800, 2450, 8300, 10900, 14300, 17900]
    base = precios[tipo] if 0 <= tipo < len(precios) else 0

    if pais == "Argentina":
        return base

    incrementos = {
        "Bolivia": 0.20,
        "Paraguay": 0.20,
        "Uruguay_Montevideo": 0.20,
        "Chile": 0.25,
        "Uruguay": 0.25,
        "Brasil": (
            0.25
            if int(cp[0]) in range(0, 4)
            else 0.30 if int(cp[0]) in range(4, 8) else 0.20
        ),
        "Otros": 0.50,
    }
    incremento = incrementos.get(pais, 0.50)
    return int(base * (1 + incremento))


def calcular_importe_final(inicial, tipo_pago):
    return int(inicial * 0.90) if tipo_pago == 1 else inicial


# Función para leer un envío del archivo binario
def leer_envio(f):
    registro = f.read(TAMANIO_REGISTRO)
    if not registro:
        raise EOFError
    cp, direccion, tipo_envio, tipo_pago, final = struct.unpack(
        FORMATO_BINARIO, registro
    )
    return {
        "cp": cp.decode("utf-8").strip("\x00"),
        "direccion": direccion.decode("utf-8").strip("\x00"),
        "tipo_envio": tipo_envio,
        "tipo_pago": tipo_pago,
        "final": final,
    }


# Función para escribir un envío en el archivo binario
def escribir_envio(f, envio):
    registro = struct.pack(
        FORMATO_BINARIO,
        envio["cp"].encode("utf-8"),
        envio["direccion"].encode("utf-8"),
        envio["tipo_envio"],
        envio["tipo_pago"],
        envio["final"],
    )
    f.write(registro)


# Función para cargar los datos desde un CSV y guardarlos en un archivo binario
def cargar_desde_csv(archivo_csv, archivo_binario):
    with open(archivo_csv, "r") as csvfile, open(archivo_binario, "wb") as binfile:
        reader = csv.reader(csvfile)
        next(reader)  # Saltar la primera línea descriptiva
        for row in reader:
            cp = row[0].strip()
            direccion = row[1].strip()
            tipo_envio = int(row[2])
            tipo_pago = int(row[3])
            pais = obtener_pais(cp)
            inicial = calcular_importe_inicial(tipo_envio, pais, cp)
            final = calcular_importe_final(inicial, tipo_pago)
            envio = {
                "cp": cp,
                "direccion": direccion,
                "tipo_envio": tipo_envio,
                "tipo_pago": tipo_pago,
                "final": final,
            }
            escribir_envio(binfile, envio)


# Función para contar los envíos por tipo y forma de pago
def contar_envios_por_tipo_y_pago(archivo_binario):
    matriz = [[0] * 2 for _ in range(7)]
    with open(archivo_binario, "rb") as f:
        while True:
            try:
                envio = leer_envio(f)
                matriz[envio["tipo_envio"]][envio["tipo_pago"] - 1] += 1
            except EOFError:
                break
    for i in range(7):
        for j in range(2):
            if matriz[i][j] > 0:
                print(f"Tipo {i}, Pago {j+1}: {matriz[i][j]}")


# Función para calcular el importe promedio de los envíos
def calcular_promedio_importe(archivo_binario):
    total_importe = 0
    cantidad = 0
    envios = []
    with open(archivo_binario, "rb") as f:
        while True:
            try:
                envio = leer_envio(f)
                total_importe += envio["final"]
                cantidad += 1
                envios.append(envio)
            except EOFError:
                break
    promedio = total_importe / cantidad if cantidad > 0 else 0
    print(f"Importe promedio: {promedio:.2f}")

    # Generar arreglo de envíos por encima del promedio
    envios_mayores_al_promedio = [
        envio for envio in envios if envio["final"] > promedio
    ]

    # Ordenar los envíos por código postal usando Shellsort
    shell_sort(envios_mayores_al_promedio)

    # Mostrar los envíos ordenados
    for envio in envios_mayores_al_promedio:
        print(envio)


# Algoritmo Shellsort para ordenar envíos por código postal
def shell_sort(envios):
    n = len(envios)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = envios[i]
            j = i
            while j >= gap and envios[j - gap]["cp"] > temp["cp"]:
                envios[j] = envios[j - gap]
                j -= gap
            envios[j] = temp
        gap //= 2


# Función auxiliar para determinar el país según el código postal
def obtener_pais(cp):
    if len(cp) == 8 and cp[0].isalpha() and cp[1:5].isdigit() and cp[5:8].isalpha():
        return "Argentina"
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


# Función principal para interactuar con el usuario
def main():
    archivo_binario = "envios.bin"
    archivo_csv = "envios-tp4.csv"

    while True:
        print("\nMenú:")
        print("1. Cargar envíos desde el archivo CSV y crear binario")
        print("2. Mostrar envíos por tipo y pago")
        print("3. Calcular promedio de importes")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            cargar_desde_csv(archivo_csv, archivo_binario)
        elif opcion == "2":
            contar_envios_por_tipo_y_pago(archivo_binario)
        elif opcion == "3":
            calcular_promedio_importe(archivo_binario)
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción inválida, intente de nuevo.")


if __name__ == "__main__":
    main()
