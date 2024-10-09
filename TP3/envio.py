import re
import pickle

class Envio:
    def __init__(self, cp, direccion, tipo_envio, tipo_pago):
        self.cp = cp
        self.direccion = direccion.rstrip(".")
        self.tipo_envio = tipo_envio
        self.tipo_pago = tipo_pago
        self.pais = self.obtener_pais()
        self.inicial = self.calcular_importe_inicial()
        self.final = self.calcular_importe_final()

    def escribir_en_archivo_binario(self, archivo_binario):
        with open(archivo_binario, "ab") as f:
            pickle.dump(self, f)
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
        if self.cp[0] == "A":
            return "Salta"
        elif self.cp[0] == "B":
            return "Buenos Aires"
        elif self.cp[0] == "C":
            return "Capital Federal"
        elif self.cp[0] == "D":
            return "San Luis"
        elif self.cp[0] == "E":
            return "Entre Ríos"
        elif self.cp[0] == "F":
            return "La Rioja"
        elif self.cp[0] == "G":
            return "Santiago del Estero"
        elif self.cp[0] == "H":
            return "Chaco"
        elif self.cp[0] == "J":
            return "San Juan"
        elif self.cp[0] == "K":
            return "Catamarca"
        elif self.cp[0] == "L":
            return "La Pampa"
        elif self.cp[0] == "M":
            return "Mendoza"
        elif self.cp[0] == "N":
            return "Misiones"
        elif self.cp[0] == "P":
            return "Formosa"
        elif self.cp[0] == "Q":
            return "Neuquén"
        elif self.cp[0] == "R":
            return "Río Negro"
        elif self.cp[0] == "S":
            return "Santa Fe"
        elif self.cp[0] == "T":
            return "Tucumán"
        elif self.cp[0] == "U":
            return "Chubut"
        elif self.cp[0] == "V":
            return "Tierra del Fuego"
        elif self.cp[0] == "W":
            return "Corrientes"
        elif self.cp[0] == "X":
            return "Córdoba"
        elif self.cp[0] == "Y":
            return "Jujuy"
        elif self.cp[0] == "Z":
            return "Santa Cruz"
        else:
            return "No aplica"

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

