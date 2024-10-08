import struct

# Estructura binaria: CP (9 bytes), Dirección (20 bytes), Tipo Envío (int, 4 bytes), Tipo Pago (int, 4 bytes), Importe Final (int, 4 bytes)
FORMATO_BINARIO = "9s20siii"  # 'i' se utiliza para enteros de 32 bits


class Envio:
    def __init__(self, cp, direccion, tipo_envio, tipo_pago):
        self.cp = cp
        self.direccion = direccion.rstrip(".")
        self.tipo_envio = tipo_envio
        self.tipo_pago = tipo_pago
        self.pais = self.obtener_pais()
        self.inicial = self.calcular_importe_inicial()
        self.final = self.calcular_importe_final()

    def obtener_pais(self):
        if (
            len(self.cp) == 8
            and self.cp[0].isalpha()
            and self.cp[1:5].isdigit()
            and self.cp[5:8].isalpha()
        ):
            return "Argentina"
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
        precios = [1100, 1800, 2450, 8300, 10900, 14300, 17900]
        base = precios[self.tipo_envio] if 0 <= self.tipo_envio < len(precios) else 0
        if self.pais == "Argentina":
            return base
        incrementos = {
            "Bolivia": 0.20,
            "Paraguay": 0.20,
            "Chile": 0.25,
            "Uruguay": 0.25,
            "Brasil": 0.25,
        }
        incremento = incrementos.get(self.pais, 0.50)
        return int(base * (1 + incremento))

    def calcular_importe_final(self):
        return int(self.inicial * 0.90) if self.tipo_pago == 1 else self.inicial

    def __str__(self):
        return f"CP: {self.cp}, Dirección: {self.direccion}, Tipo Envío: {self.tipo_envio}, Tipo Pago: {self.tipo_pago}, País: {self.pais}, Importe Inicial: {self.inicial}, Importe Final: {self.final}"

    @staticmethod
    def leer_de_binario(f):
        registro = f.read(struct.calcsize(FORMATO_BINARIO))
        if not registro:
            raise EOFError
        cp, direccion, tipo_envio, tipo_pago, final = struct.unpack(
            FORMATO_BINARIO, registro
        )
        envio = Envio(
            cp.decode("utf-8").strip("\x00"),
            direccion.decode("utf-8").strip("\x00"),
            tipo_envio,
            tipo_pago,
        )
        envio.final = final
        return envio

    def escribir_en_binario(self, f):
        registro = struct.pack(
            FORMATO_BINARIO,
            self.cp.encode("utf-8"),
            self.direccion.encode("utf-8"),
            self.tipo_envio,
            self.tipo_pago,
            self.final,
        )
        f.write(registro)
