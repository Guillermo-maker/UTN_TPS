import re
import pickle
from envio import Envio
import csv

envios = []
tipo_control = "HC"
archivo_nombre = "envios-tp4.csv"


def cargar_envios():
    global envios, tipo_control
    print("Cargando datos desde el archivo...")
    if envios:
        confirmar = input(
            "Ya existen datos cargados. ¿Desea eliminar los datos actuales y volver a cargar? (s/n): "
        )
        if confirmar.lower() != "s":
            return
    envios = leer_envios_binario('envios.bin')

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
    envio = Envio(cp, direccion, tipo_envio, tipo_pago)
    envios.append(envio)
    with open('envios.bin', "wb") as f:
        pickle.dump(envios, f)

def mostrar_envios(archivo_binario, m):
    try:
        envios = []
        with open(archivo_binario, "rb") as f:
            while True:
                try:
                    envio = pickle.load(f)
                    envios.append(envio)
                except EOFError:
                    break

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
    except FileNotFoundError:
        print("No se encontró el archivo binario")

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
        next(reader)  # Saltar la primera fila
        next(reader)  # Saltar la segunda fila
        with open(archivo_binario, "wb") as f:
            for row in reader:
                envio = Envio(row[0], row[1], int(row[2]), int(row[3]))
                pickle.dump(envio, f)


def leer_envios_binario(archivo_binario):
    try:
        with open(archivo_binario, "rb") as f:
            envios = pickle.load(f)
            return envios
    except FileNotFoundError:
        print("No se encontró el archivo binario.")
        return []

def procesar_opciones():
    global tipo_control, envios

    while True:
        print("Menú:")
        print(
            "1. Cargar envíos desde el archivo: Carga todos los envíos desde el archivo binario y los almacena en memoria.")
        print(
            "2. Buscar un envío por dirección postal: Busca y muestra un envío que coincide con una dirección postal específica.")
        print(
            "3. Contar envíos según tipo de envío y forma de pago: Cuenta y muestra la cantidad de envíos según su tipo de envío y forma de pago.")
        print(
            "4. Totalizar envíos según tipo de envío y forma de pago: Totaliza y muestra la cantidad de envíos según su tipo de envío y forma de pago.")
        print(
            "5. Calcular importe promedio y mostrar envíos con importe mayor al promedio: Calcula el importe promedio de los envíos y muestra los envíos que tienen un importe mayor al promedio.")
        print("6. Cargar un nuevo envío: Permite cargar un nuevo envío manualmente y lo agrega a la lista de envíos.")
        print(
            "7. Mostrar todos los envíos ordenados por código postal: Muestra todos los envíos ordenados por código postal utilizando el método Shell Sort.")
        print("8. Salir: Sale del programa.")

        opcion = str(input("Seleccione una opción: "))

        if opcion == "1":
            archivo_csv = input("Ingrese el nombre del archivo CSV: ")
            cargar_desde_csv(archivo_csv, 'envios.bin')

        elif opcion == "2":
            cargar_envio()
        elif opcion == "3":
            m = int(input("¿Cuántos registros desea mostrar? (0 para todos): "))
            mostrar_envios('envios.bin', m)
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
