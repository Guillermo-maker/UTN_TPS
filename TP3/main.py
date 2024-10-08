import csv
import struct
from envio import Envio

archivo_nombre_binario = "envios.bin"
archivo_csv = "envios-tp4.csv"

# Tamaño del registro binario
TAMANIO_REGISTRO = struct.calcsize("9s20siib")


def cargar_desde_csv(archivo_csv, archivo_binario):
    with open(archivo_csv, "r") as csvfile, open(archivo_binario, "wb") as binfile:
        reader = csv.reader(csvfile)
        next(reader)  # Saltar la primera línea del timestamp
        next(reader)  # Saltar la segunda línea del encabezado
        for row in reader:
            # Asignar cada valor a sus respectivas variables
            cp = row[0].strip()  # Código postal
            direccion = row[1].strip()  # Dirección
            tipo_envio = int(row[2])  # Tipo de envío
            forma_pago = int(row[3])  # Forma de pago

            # Crear un objeto Envio y escribirlo en el archivo binario
            envio = Envio(cp, direccion, tipo_envio, forma_pago)
            envio.escribir_en_binario(binfile)


def mostrar_envios_binarios(archivo_binario):
    with open(archivo_binario, "rb") as f:
        while True:
            try:
                envio = Envio.leer_de_binario(f)
                print(envio)
            except EOFError:
                break


def buscar_por_cp(archivo_binario, cp):
    with open(archivo_binario, "rb") as f:
        while True:
            try:
                envio = Envio.leer_de_binario(f)
                if envio.cp == cp:
                    print(envio)
                    return
            except EOFError:
                break
    print(f"No se encontró un envío con el CP: {cp}")


def buscar_por_direccion(archivo_binario, direccion):
    with open(archivo_binario, "rb") as f:
        while True:
            try:
                envio = Envio.leer_de_binario(f)
                if envio.direccion == direccion:
                    print(envio)
                    return
            except EOFError:
                break
    print(f"No se encontró un envío con la dirección: {direccion}")


def procesar_opciones():
    while True:
        print("\nMenú:")
        print("1. Cargar envíos desde archivo CSV y crear archivo binario")
        print("2. Mostrar todos los envíos")
        print("3. Buscar por código postal")
        print("4. Buscar por dirección")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            cargar_desde_csv(archivo_csv, archivo_nombre_binario)
        elif opcion == "2":
            mostrar_envios_binarios(archivo_nombre_binario)
        elif opcion == "3":
            cp = input("Ingrese el código postal a buscar: ")
            buscar_por_cp(archivo_nombre_binario, cp)
        elif opcion == "4":
            direccion = input("Ingrese la dirección a buscar: ")
            buscar_por_direccion(archivo_nombre_binario, direccion)
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción no válida, intente de nuevo.")


if __name__ == "__main__":
    procesar_opciones()
