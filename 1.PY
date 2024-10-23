# Función para leer la gramática desde un archivo
def leer_gramatica(archivo_gramatica):
    gramatica = {}
    with open(archivo_gramatica, 'r') as f:
        for linea in f:
            # Separar el lado izquierdo y el derecho de cada regla
            no_terminal, produccion = linea.split('→')
            no_terminal = no_terminal.strip()
            produccion = produccion.strip().split()
            if no_terminal not in gramatica:
                gramatica[no_terminal] = []
            gramatica[no_terminal].append(produccion)
    return gramatica

# Función para calcular el conjunto de PRIMEROS
def calcular_primeros(gramatica):
    primeros = {}
    
    # Inicialización de los conjuntos vacíos
    for no_terminal in gramatica:
        primeros[no_terminal] = set()
    
    # Calculo de PRIMEROS
    for no_terminal in gramatica:
        obtener_primeros(no_terminal, gramatica, primeros)
    
    return primeros

def obtener_primeros(no_terminal, gramatica, primeros):
    for produccion in gramatica[no_terminal]:
        simbolo = produccion[0]
        
        if simbolo.islower() or simbolo.isdigit():  # Es terminal
            primeros[no_terminal].add(simbolo)
        elif simbolo.isupper():  # Es no terminal
            if simbolo != no_terminal:
                obtener_primeros(simbolo, gramatica, primeros)
                primeros[no_terminal].update(primeros[simbolo])
        elif simbolo == 'ε':  # Si es ε (epsilon)
            primeros[no_terminal].add('ε')

# Función para calcular el conjunto de SIGUIENTES
def calcular_siguientes(gramatica, primeros):
    siguientes = {}
    
    # Inicializar SIGUIENTES con el símbolo inicial conteniendo el símbolo $
    for no_terminal in gramatica:
        siguientes[no_terminal] = set()
    siguientes['S'].add('$')  # Asumimos que S es el símbolo inicial
    
    # Calculo de SIGUIENTES
    for no_terminal in gramatica:
        obtener_siguientes(no_terminal, gramatica, primeros, siguientes)
    
    return siguientes

def obtener_siguientes(no_terminal, gramatica, primeros, siguientes):
    for nt, producciones in gramatica.items():
        for produccion in producciones:
            if no_terminal in produccion:
                indice = produccion.index(no_terminal)
                if indice + 1 < len(produccion):  # Si hay un símbolo después del actual
                    siguiente = produccion[indice + 1]
                    if siguiente.islower() or siguiente.isdigit():
                        siguientes[no_terminal].add(siguiente)
                    else:
                        siguientes[no_terminal].update(primeros[siguiente])
                        if 'ε' in primeros[siguiente]:
                            siguientes[no_terminal].update(siguientes[nt])
                else:
                    siguientes[no_terminal].update(siguientes[nt])

def calcular_predicciones(gramatica, primeros, siguientes):
    predicciones = {}

    for no_terminal, producciones in gramatica.items():
        predicciones[no_terminal] = []
        for produccion in producciones:
            conjunto_prediccion = set()

            # Si el primer símbolo de la producción es terminal o ε
            if produccion[0].islower() or produccion[0].isdigit() or produccion[0] == 'ε':
                conjunto_prediccion.add(produccion[0])
            
            # Si el primer símbolo es un no terminal
            elif produccion[0].isupper():
                conjunto_prediccion.update(primeros[produccion[0]])
                # Si puede derivar en ε, agregar SIGUIENTES del no terminal
                if 'ε' in primeros[produccion[0]]:
                    conjunto_prediccion.remove('ε')
                    conjunto_prediccion.update(siguientes[no_terminal])
            
            # Si la producción es directamente ε
            if 'ε' in produccion:
                conjunto_prediccion.update(siguientes[no_terminal])

            predicciones[no_terminal].append(conjunto_prediccion)

    return predicciones

def main():
    archivo_gramatica = 'gramatica2.txt'  
    gramatica = leer_gramatica(archivo_gramatica)
    
    primeros = calcular_primeros(gramatica)
    print("Conjuntos de PRIMEROS:", primeros)
    
    siguientes = calcular_siguientes(gramatica, primeros)
    print("Conjuntos de SIGUIENTES:", siguientes)

    predicciones = calcular_predicciones(gramatica, primeros, siguientes)
    print("Conjuntos de PREDICCIONES:")
    for no_terminal, conjunto_prediccion in predicciones.items():
        for i, prediccion in enumerate(conjunto_prediccion):
            print(f"{no_terminal} → {gramatica[no_terminal][i]}: {prediccion}")

if __name__ == '__main__':
    main()
