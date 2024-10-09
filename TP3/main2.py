import re
import pickle
from envio import Envio
import csv

def crear_archivo_binario():
    archivo_csv = input("Ingrese el nombre del archivo CSV: ")
    confirmar = input("¿Está seguro de crear un nuevo archivo binario? (s/n): ")
    if confirmar.lower() != "s":
        return
    with open(archivo_csv, "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Saltar la primera fila
        next(reader)  # Saltar la segunda fila
        with open('envios.bin', "wb") as f:
            for row in reader:
                envio = Envio(row[0], row[1], int(row[2]), int(row[3]))
                pickle.dump(envio, f)

def cargar_envio():
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
    with open('envios.bin', "ab") as f:
        pickle.dump(envio, f)

def mostrar_envios():
    try:
        with open('envios.bin', "rb") as f:
            while True:
                try:
                    envio = pickle.load(f)
                    print(envio)
                except EOFError:
                    break
    except FileNotFoundError:
        print("No se encontró el archivo binario")

def buscar_cp():
    cp = input("Ingrese el código postal a buscar: ")
    try:
        with open('envios.bin', "rb") as f:
            contador = 0
            while True:
                try:
                    envio = pickle.load(f) # tiene un file pointer que lee la siguiente linea en cada vuelta
                    if envio.cp == cp:
                        print(envio)
                        contador += 1
                except EOFError: # eoferror es cuando encuentra el final del archivo
                    break
            print(f"Se encontraron {contador} registros con el código postal {cp}")
    except FileNotFoundError:
        print("No se encontró el archivo binario")

def buscar_direccion():
    d = input("Ingrese la dirección a buscar: ")
    try:
        with open('envios.bin', "rb") as f:
            while True:
                try:
                    envio = pickle.load(f)
                    if envio.direccion == d:
                        print(envio)
                        return
                except EOFError:
                    break
            print("No se encontró un envío con esa dirección")
    except FileNotFoundError:
        print("No se encontró el archivo binario")

def contar_envios():
    conteos = []
    for i in range(7):
        conteos.append([0, 0])
    try:
        with open('envios.bin', "rb") as f:
            while True:
                try:
                    envio = pickle.load(f)
                    conteos[envio.tipo_envio][envio.tipo_pago - 1] += 1
                except EOFError:
                    break
        for i in range(7):
            for j in range(2):
                if conteos[i][j] > 0:
                    print(f"Tipo de envío {i}, forma de pago {j+1}: {conteos[i][j]}")
    except FileNotFoundError:
        print("No se encontró el archivo binario")

def totalizar_envios():
    total_tipo_envio = [0] * 7
    total_forma_pago = [0] * 2
    try:
        with open('envios.bin', "rb") as f:
            while True:
                try:
                    envio = pickle.load(f)
                    total_tipo_envio[envio.tipo_envio] += 1
                    total_forma_pago[envio.tipo_pago - 1] += 1
                except EOFError:
                    break
        for i in range(7):
            print(f"Tipo de envío {i}: {total_tipo_envio[i]}")
        for j in range(2):
            print(f"Forma de pago {j+1}: {total_forma_pago[j]}")
    except FileNotFoundError:
        print("No se encontró el archivo binario")

def calcular_importe_promedio():
    importe_total = 0
    contador =  0
    try:
        with open('envios.bin', "rb") as f:
            while True:
                try:
                    envio = pickle.load(f)
                    importe_total += envio.final
                    contador += 1
                except EOFError:
                    break

        if contador > 0:
            promedio = importe_total / contador
        else:
            promedio = 0

        envios_mayores_al_promedio = []
        with open('envios.bin', "rb") as f:
            while True:
                try:
                    envio = pickle.load(f)
                    if envio.final > promedio:
                        envios_mayores_al_promedio.append(envio)
                except EOFError:
                    break
        # ordenamiento por Shell Sort
        gap = len(envios_mayores_al_promedio) // 2
        while gap > 0:
            for i in range(gap, len(envios_mayores_al_promedio)):
                temp = envios_mayores_al_promedio[i]
                j = i
                while j >= gap and envios_mayores_al_promedio[j - gap].cp > temp.cp:
                    envios_mayores_al_promedio[j] = envios_mayores_al_promedio[j - gap]
                    j -= gap
                envios_mayores_al_promedio[j] = temp
            gap //= 2
        for envio in envios_mayores_al_promedio:
            print(envio)
        print(f"Importe promedio: {promedio}")
    except FileNotFoundError:
        print("No se encontró el archivo binario")

def procesar_opciones():
    while True:
        print("Menú:")
        print("1. Crear archivo binario")
        print("2. Cargar envío")
        print("3. Mostrar envíos")
        print("4. Buscar código postal")
        print("5. Buscar dirección")
        print("6. Contar envíos")
        print("7. Totalizar envíos")
        print("8. Calcular importe promedio")
        print("9. Salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            crear_archivo_binario()
        elif opcion == "2":
            cargar_envio()
        elif opcion == "3":
            mostrar_envios()
        elif opcion == "4":
            buscar_cp()
        elif opcion == "5":
            buscar_direccion()
        elif opcion == "6":
            contar_envios()
        elif opcion == "7":
            totalizar_envios()
        elif opcion == "8":
            calcular_importe_promedio()
        elif opcion == "9":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")

if __name__ == "__main__":
    procesar_opciones()