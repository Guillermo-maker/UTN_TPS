import re

def validar_direccion_hard_control(direccion):
    # Reemplazar punto al final por espacio en blanco
    direccion = direccion.rstrip('.') + ' '

    # Validación específica para Hard Control
    if not re.search(r'\d', direccion):  # Debe contener al menos un dígito
        return False
    if re.search(r'[^a-zA-Z0-9 ]', direccion):  # Solo letras, dígitos y espacio
        return False
    if re.search(r'[A-Z]{2}', direccion):  # No puede haber dos mayúsculas seguidas
        return False
    if not re.search(r'\b\d+\b', direccion):  # Debe haber al menos una palabra compuesta solo por dígitos
        return False
    return True

# Contadores para validos e invalidos
cedvalid = 0
cedinvalid = 0

# Lectura del archivo envios25.txt
with open('envios25.txt', 'r') as archivo:
    lineas = archivo.readlines()

# Procesamiento de timestamp (en este caso, asumiendo solo la primera línea como timestamp)
timestamp = lineas[0].strip()
control = ""

if 'HC' in timestamp:
    control = 'Hard Control'
else:
    'Soft Control'

# Iterar sobre las líneas de envíos
for linea in lineas[1:]:
    cp = linea[:9].strip()  # Código postal, primeros 9 caracteres
    direccion = linea[9:29].strip()  # Dirección, siguientes 20 caracteres

    # Validar dirección según el tipo de control
    if control == 'Hard Control':
        es_valida = validar_direccion_hard_control(direccion)
    else:
        es_valida = True  # Para Soft Control, cualquier dirección es válida

    if es_valida:
        cedvalid += 1
    else:
        cedinvalid += 1

# Mostrar resultados
print(f' (r1) - Tipo de control de direcciones:', control)
print(' (r2) - Cantidad de envios con direccion valida:', cedvalid)
print(' (r3) - Cantidad de envios con direccion no valida:', cedinvalid)
import re

def validar_direccion_hard_control(direccion):
    # Reemplazar punto al final por espacio en blanco
    direccion = direccion.rstrip('.') + ' '

    # Validación específica para Hard Control
    if not re.search(r'\d', direccion):  # Debe contener al menos un dígito
        return False
    if re.search(r'[^a-zA-Z0-9 ]', direccion):  # Solo letras, dígitos y espacio
        return False
    if re.search(r'[A-Z]{2}', direccion):  # No puede haber dos mayúsculas seguidas
        return False
    if not re.search(r'\b\d+\b', direccion):  # Debe haber al menos una palabra compuesta solo por dígitos
        return False
    return True

# Contadores para validos e invalidos
cedvalid = 0
cedinvalid = 0

# Lectura del archivo envios25.txt
with open('envios25.txt', 'r') as archivo:
    lineas = archivo.readlines()

# Procesamiento de timestamp (en este caso, asumiendo solo la primera línea como timestamp)
timestamp = lineas[0].strip()
control = ""

if 'HC' in timestamp:
    control = 'Hard Control'
else:
    'Soft Control'

# Iterar sobre las líneas de envíos
for linea in lineas[1:]:
    cp = linea[:9].strip()  # Código postal, primeros 9 caracteres
    direccion = linea[9:29].strip()  # Dirección, siguientes 20 caracteres

    # Validar dirección según el tipo de control
    if control == 'Hard Control':
        es_valida = validar_direccion_hard_control(direccion)
    else:
        es_valida = True  # Para Soft Control, cualquier dirección es válida

    if es_valida:
        cedvalid += 1
    else:
        cedinvalid += 1

# Mostrar resultados
print(f' (r1) - Tipo de control de direcciones:', control)
print(' (r2) - Cantidad de envios con direccion valida:', cedvalid)
print(' (r3) - Cantidad de envios con direccion no valida:', cedinvalid)
