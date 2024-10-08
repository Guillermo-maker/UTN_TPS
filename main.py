import re

from envio import Envio

envios = []
tipo_control = "HC"
archivo_nombre = "envios-tp3.txt"


def cargar_envios():
    global envios, tipo_control
    print("Cargando datos desde el archivo...")
    if envios:
        confirmar = input(
            "Ya existen datos cargados. ¿Desea eliminar los datos actuales y volver a cargar? (s/n): "
        )
        if confirmar.lower() != "s":
            return
    with open(archivo_nombre, "r") as archivo:
        lineas = archivo.readlines()

    # Procesar timestamp
    timestamp = lineas[0].strip()
    if "HC" in timestamp:
        tipo_control = "Hard Control"
    else:
        tipo_control = "Soft Control"


    envios = []
    for linea in lineas[1:]:
        cp = linea[:9].strip()
        direccion = linea[9:29].strip()
        tipo_envio = int(linea[29])
        tipo_pago = int(linea[30])
        envios.append(Envio(cp, direccion, tipo_envio, tipo_pago))


def cargar_envio():
    global envios
    cp = input("Ingrese el código postal: ")
    direccion = input("Ingrese la dirección: ")
    tipo_envio = int(input("Ingrese el tipo de envío (0-6): "))
    while tipo_envio < 0 or tipo_envio > 6:
        tipo_envio = int(
            input("Tipo de envío inválido. Ingrese el tipo de envío (0-6): ")
        )
    tipo_pago = int(input("Ingrese el tipo de pago (1 o 2): "))
    while tipo_pago not in [1, 2]:
        tipo_pago = int(
            input("Tipo de pago inválido. Ingrese el tipo de pago (1 o 2): ")
        )
    envios.append(Envio(cp, direccion, tipo_envio, tipo_pago))


def mostrar_envios(m):
    global envios
    n = len(envios)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = envios[i]
            j = i
            while j >= gap and envios[j - gap].cp > temp.cp:
                envios[j] = envios[j - gap]
                j -= gap
            envios[j] = temp
        gap //= 2

    # Mostrar los envíos
    if m == 0:
        for envio in envios:
            print(envio)
    else:
        for envio in envios[:m]:
            print(envio)

def buscar_direccion(d, e):
    for envio in envios:
        if envio.direccion == d and envio.tipo_envio == e:
            print(envio)
            return
    print("No se encontró un envío con esa dirección y tipo.")


def buscar_cp(cp):
    for envio in envios:
        if envio.cp == cp:
            envio.tipo_pago = 2 if envio.tipo_pago == 1 else 1
            print(envio)
            return
    print("No se encontró un envío con ese código postal.")


def cargar_desde_csv(archivo_csv, archivo_binario):
    with open(archivo_csv, "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Saltar la primera línea de descriptores
        for row in reader:
            envio = Envio(row[0], row[1], int(row[2]), int(row[3]))
            envio.escribir_en_archivo_binario(archivo_binario)


def leer_envios_binario(archivo_binario):
    with open(archivo_binario, "rb") as f:
        while True:
            try:
                # Desempaquetar los datos desde binario
                envio = leer_envio(f)
                print(envio)
            except EOFError:
                break


def procesar_opciones():
    global tipo_control, envios

    while True:
        print("\nMenú:")
        print("1. Cargar envíos desde el archivo")
        print("2. Cargar un nuevo envío")
        print("3. Mostrar todos los envíos ordenados por código postal")
        print("4. Buscar por dirección y tipo de envío")
        print("5. Buscar por código postal y modificar tipo de pago")
        print("6. Contar envíos según tipo de control")
        print("7. Acumular importes finales según tipo de control")
        print("8. Tipo de envío con mayor importe acumulado")
        print("9. Importe promedio y cantidad de envíos por debajo")
        print("0. Salir")

        opcion = str(input("Seleccione una opción: "))

        if opcion == "1":
            archivo_csv = input("Ingrese el nombre del archivo CSV: ")
            cargar_desde_csv(archivo_csv, 'envios.bin')

        elif opcion == "2":
            cargar_envio()
        elif opcion == "3":
            m = int(input("¿Cuántos registros desea mostrar? (0 para todos): "))
            mostrar_envios(m)
        elif opcion == "4":
            d = input("Ingrese la dirección a buscar: ")
            e = int(input("Ingrese el tipo de envío a buscar (0-6): "))
            buscar_direccion(d, e)
        elif opcion == "5":
            cp = input("Ingrese el código postal a buscar: ")
            buscar_cp(cp)
        elif opcion == "6":
            if not envios:
                print("No se han cargado datos aún.")
            

            conteos = [0] * 7
            if tipo_control == "Hard Control":
                for envio in envios:
                    if envio.validar_direccion_hard_control():
                        conteos[envio.tipo_envio] += 1
            else:  # Soft Control
                for envio in envios:
                    conteos[envio.tipo_envio] += 1

            for i in range(7):
                print(f"Cantidad de envíos para tipo {i}: {conteos[i]}")

        elif opcion == "7":
            if not envios:
                print("No se han cargado datos aún.")
                

            acumuladores = [0] * 7
            if tipo_control == "Hard Control":
                for envio in envios:
                    if envio.validar_direccion_hard_control():
                        acumuladores[envio.tipo_envio] += envio.final
            else:  # Soft Control
                for envio in envios:
                    acumuladores[envio.tipo_envio] += envio.final

            for i in range(7):
                print(f"Importe acumulado para tipo {i}: {acumuladores[i]}")

        elif opcion == "8":
            if not envios:
                print("No se han cargado datos aún.")
                

            if tipo_control == "Hard Control":
                acumuladores = [0] * 7
                for envio in envios:
                    if envio.validar_direccion_hard_control():
                        acumuladores[envio.tipo_envio] += envio.final
            else:  # Soft Control
                acumuladores = [0] * 7
                for envio in envios:
                    acumuladores[envio.tipo_envio] += envio.final

            max_importe = max(acumuladores)
            tipo_max_importe = acumuladores.index(max_importe)
            total_importe = sum(acumuladores)
            porcentaje = (max_importe / total_importe) * 100 if total_importe > 0 else 0

            print(f"Tipo de envío con mayor importe acumulado: {tipo_max_importe}")
            print(f"Importe mayor: {max_importe}")
            print(f"Porcentaje sobre el total: {porcentaje:.2f}%")

        elif opcion == "9":
            if not envios:
                print("No se han cargado datos aún.")
                

            if not envios:
                print("No se han cargado datos aún.")
                

            total_importe = sum(envio.final for envio in envios)
            promedio = total_importe / len(envios) if envios else 0
            menor_al_promedio = sum(1 for envio in envios if envio.final < promedio)

            print(f"Importe final promedio: {promedio:.2f}")
            print(
                f"Cantidad de envíos con importe menor al promedio: {menor_al_promedio}"
            )

        elif opcion == "0":
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Inténtelo de nuevo.")


if __name__ == "__main__":
    procesar_opciones()
