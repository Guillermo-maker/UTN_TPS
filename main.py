import re

class Envio:
    def __init__(self, cp, direccion, tipo_envio, tipo_pago):
        self.cp = cp
        self.direccion = direccion
        self.tipo_envio = tipo_envio
        self.tipo_pago = tipo_pago
        self.pais = self.obtener_pais()
        self.inicial = self.calcular_importe_inicial()
        self.final = self.calcular_importe_final()

    def obtener_precio_nacional(self):
        precios = [1100, 1800, 2450, 8300, 10900, 14300, 17900]
        return precios[self.tipo_envio] if 0 <= self.tipo_envio < len(precios) else 0

    def obtener_incremento_internacional(self):
        pais = self.pais
        cp = self.cp
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
            return 0.50  # Otros países

    def validar_direccion_hard_control(self):
        direccion = self.direccion.rstrip(".") + " "
        if not re.search(r"\d", direccion):
            return False
        if re.search(r"[^a-zA-Z0-9 ]", direccion):
            return False
        if re.search(r"[A-Z]{2}", direccion):
            return False
        if not re.search(r"\b\d+\b", direccion):
            return False
        return True

    def obtener_provincia(self):
        provincias = {
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
        return provincias.get(self.cp[0], "No aplica")

    def obtener_pais(self):
        provincia = self.obtener_provincia()
        if (
            len(self.cp) == 8
            and self.cp[0].isalpha()
            and self.cp[1:5].isdigit()
            and self.cp[5:8].isalpha()
        ):
            return "Argentina" if provincia != "No aplica" else "Otros"
        elif len(self.cp) == 4 and self.cp.isdigit():
            return "Bolivia"
        elif (
            len(self.cp) == 9
            and self.cp[:5].isdigit()
            and self.cp[5] == "-"
            and self.cp[6:].isdigit()
        ):
            return "Brasil"
        elif len(self.cp) == 7 and self.cp.isdigit():
            return "Chile"
        elif len(self.cp) == 6 and self.cp.isdigit():
            return "Paraguay"
        elif len(self.cp) == 5 and self.cp.isdigit():
            return "Uruguay"
        else:
            return "Otros"

    def calcular_importe_inicial(self):
        base = self.obtener_precio_nacional()
        if self.pais == "Argentina":
            return base
        incremento = self.obtener_incremento_internacional()
        return int(base * (1 + incremento))

    def calcular_importe_final(self):
        if self.tipo_pago == 1:
            return int(self.inicial * 0.90)  # 10% de descuento
        return self.inicial

    def __str__(self):
        return f"CP: {self.cp}, Dirección: {self.direccion}, Tipo Envio: {self.tipo_envio}, Tipo Pago: {self.tipo_pago}, País: {self.pais}, Importe Inicial: {self.inicial}, Importe Final: {self.final}"


envios = []
tipo_control = "HC"
archivo_nombre = "envios100HC.txt"

def cargar_envios():
    global envios, tipo_control
    print("Cargando datos desde el archivo...")
    if envios:
        confirmar = input("Ya existen datos cargados. ¿Desea eliminar los datos actuales y volver a cargar? (s/n): ")
        if confirmar.lower() != 's':
            return
    with open(archivo_nombre, "r") as archivo:
        lineas = archivo.readlines()
    
    # Procesar timestamp
    timestamp = lineas[0].strip()
    tipo_control = "Hard Control" if "HC" in timestamp else "Soft Control"

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
        tipo_envio = int(input("Tipo de envío inválido. Ingrese el tipo de envío (0-6): "))
    tipo_pago = int(input("Ingrese el tipo de pago (1 o 2): "))
    while tipo_pago not in [1, 2]:
        tipo_pago = int(input("Tipo de pago inválido. Ingrese el tipo de pago (1 o 2): "))
    envios.append(Envio(cp, direccion, tipo_envio, tipo_pago))

def mostrar_envios(m=0):
    global envios
    envios_ordenados = sorted(envios, key=lambda x: x.cp)
    if m <= 0 or m > len(envios_ordenados):
        m = len(envios_ordenados)
    for envio in envios_ordenados[:m]:
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

        opcion = int(input("Seleccione una opción: "))

        if opcion == 1:
            cargar_envios()
        elif opcion == 2:
            cargar_envio()
        elif opcion == 3:
            m = int(input("¿Cuántos registros desea mostrar? (0 para todos): "))
            mostrar_envios(m)
        elif opcion == 4:
            d = input("Ingrese la dirección a buscar: ")
            e = int(input("Ingrese el tipo de envío a buscar (0-6): "))
            buscar_direccion(d, e)
        elif opcion == 5:
            cp = input("Ingrese el código postal a buscar: ")
            buscar_cp(cp)
        elif opcion == 6:
            if not envios:
                print("No se han cargado datos aún.")
                continue

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

        elif opcion == 7:
            if not envios:
                print("No se han cargado datos aún.")
                continue

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

        elif opcion == 8:
            if not envios:
                print("No se han cargado datos aún.")
                continue

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

        elif opcion == 9:
            if not envios:
                print("No se han cargado datos aún.")
                continue

            if not envios:
                print("No se han cargado datos aún.")
                continue

            total_importe = sum(envio.final for envio in envios)
            promedio = total_importe / len(envios) if envios else 0
            menor_al_promedio = sum(1 for envio in envios if envio.final < promedio)

            print(f"Importe final promedio: {promedio:.2f}")
            print(
                f"Cantidad de envíos con importe menor al promedio: {menor_al_promedio}"
            )

        elif opcion == 0:
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Inténtelo de nuevo.")


if __name__ == "__main__":
    procesar_opciones()
