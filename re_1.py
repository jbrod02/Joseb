import re
from collections import defaultdict

class Nodo:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor
        self.izquierda = None
        self.derecha = None
        self.hijos = []  # Para estructuras más complejas como if, while, etc.

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

class ArbolSintactico:
    def __init__(self):
        self.raiz = None

    def construir(self, tokens):
        # Mostrar si hay errores antes de construir el árbol
        if not self.detectar_errores(tokens):
            self.raiz = self._construir_arbol(tokens)
        else:
            return False  # Indicar que hubo errores
        return True  # Indicar que no hubo errores

    def detectar_errores(self, tokens):
        errores = False
        print("\n=== DETECCIÓN DE ERRORES ===")
        if tokens[0] != 'int' and tokens[0] != 'float':
            print("Error: El programa debe comenzar con una declaración de tipo ('int' o 'float').")
            errores = True
        if tokens.count('(') != tokens.count(')'):
            print("Error: Paréntesis no balanceados.")
            errores = True
        if tokens.count('{') != tokens.count('}'):
            print("Error: Llaves no balanceadas.")
            errores = True
        if not errores:
            print("No se detectaron errores sintácticos.")
        return errores

    def _construir_arbol(self, tokens):
        if not tokens:
            return None

        nodo_programa = Nodo("PROGRAMA")

        i = 0
        while i < len(tokens):
            token = tokens[i]

            if token == 'int' or token == 'float':  # Declaraciones
                declaracion = Nodo("DECLARACION")
                declaracion.agregar_hijo(Nodo("TIPO", tokens[i]))  # Tipo de variable
                i += 1
                declaracion.agregar_hijo(Nodo("IDENTIFICADOR", tokens[i]))  # Identificador
                i += 1
                if tokens[i] == '=':  # Asignación
                    i += 1
                    declaracion.agregar_hijo(Nodo("VALOR", tokens[i]))  # Valor asignado
                nodo_programa.agregar_hijo(declaracion)

            elif token == 'if':  # Condicional if
                nodo_if = Nodo("IF")
                i += 1  # Salta al paréntesis de condición
                nodo_if.agregar_hijo(Nodo("CONDICION", f"{tokens[i+1]} {tokens[i+2]} {tokens[i+3]}"))  # Condición
                i += 4  # Salta al cuerpo del if
                nodo_if.agregar_hijo(Nodo("CUERPO", "bloque de código"))
                nodo_programa.agregar_hijo(nodo_if)

            elif token == 'else':  # Condicional else
                nodo_else = Nodo("ELSE")
                nodo_else.agregar_hijo(Nodo("CUERPO", "bloque de código"))
                nodo_programa.agregar_hijo(nodo_else)

            i += 1

        return nodo_programa

    def imprimir(self, nodo=None, nivel=0, lado="RAIZ"):
        if nodo is None:
            nodo = self.raiz

        print("  " * nivel + f"{lado} -> {nodo.tipo}: {nodo.valor if nodo.valor else ''}")

        for hijo in nodo.hijos:
            self.imprimir(hijo, nivel + 1, "HIJO")

class AnalizadorLexico:
    def __init__(self):
        self.tokens = [
            ('PALABRA_CLAVE', r'\b(if|else|while|for|return|int|float|char|void|print)\b'),
            ('IDENTIFICADOR', r'\b[a-zA-Z_][a-zA-Z_0-9]*\b'),
            ('NUMERO', r'\b\d+(\.\d+)?\b'),
            ('OPERADOR', r'[\+\-\*/=<>]'),
            ('DELIMITADOR', r'[()\{\};,]'),
            ('ESPACIO', r'\s+'),  
            ('DESCONOCIDO', r'.'),  
        ]
    
    def analizar(self, codigo):
        from collections import defaultdict
        import re
        
        posicion = 0
        tokens_encontrados = defaultdict(list)
        error_encontrado = False
        
        while posicion < len(codigo):
            match = None
            for token_type, token_regex in self.tokens:
                regex = re.compile(token_regex)
                match = regex.match(codigo, posicion)
                if match:
                    if token_type != 'ESPACIO': 
                        token = match.group(0)
                        tokens_encontrados[token_type].append(token)
                    if token_type == 'DESCONOCIDO':
                        error_encontrado = True
                    posicion = match.end(0)
                    break
            if not match:
                tokens_encontrados['DESCONOCIDO'].append(codigo[posicion])
                error_encontrado = True
                posicion += 1
        
        if error_encontrado:
            print("¡Error: Se encontraron caracteres desconocidos en el código!")
        
        return tokens_encontrados

    def imprimir_tokens(self, tokens_encontrados):
        print("\n=== TOKENS ENCONTRADOS ===")
        for token_type, tokens in tokens_encontrados.items():
            tokens_string = ', '.join(tokens)
            print(f"=== {token_type} ===\n{tokens_string}\n")

if __name__ == "__main__":
    while True:
        print("\n" + "="*50)  # Separador
        modo = input("1. Deseas ingresar el código directamente\n2. Usar el código por defecto\n3. Salir del sistema\nIngresa 1, 2 o 3: ")

        if modo == '1':
            print("Por favor ingresa tu código (termina con una línea vacía):")
            lineas = []
            while True:
                try:
                    linea = input()
                    if linea == '':
                        break
                    lineas.append(linea)
                except EOFError:
                    break
            codigo_fuente = '\n'.join(lineas)
        elif modo == '2':
            codigo_fuente = """
            int main() {
                int x = 10;
                float y = 20.5;
                if (x > 0) {
                    return x;
                } else {
                    return 0;
                }
            }
            """
        elif modo == '3':
            print("Saliendo del sistema.")
            break
        else:
            print("Opción no válida. Por favor, ingresa 1, 2 o 3.")
            continue
        
        # Análisis léxico
        print("\n=== INICIANDO ANÁLISIS LÉXICO ===")
        analizador = AnalizadorLexico()
        tokens = analizador.analizar(codigo_fuente)
        analizador.imprimir_tokens(tokens)

        # Construir el árbol sintáctico
        print("\n=== CONSTRUYENDO ÁRBOL SINTÁCTICO ===")
        arbol = ArbolSintactico()
        tokens_lineales = [token for tipo, lista in tokens.items() for token in lista]  # Listar todos los tokens
        exito = arbol.construir(tokens_lineales)

        # Mostrar el árbol sintáctico solo si no hubo errores
        if exito:
            print("\n=== ÁRBOL SINTÁCTICO ===")
            arbol.imprimir()
        else:
            print("\nVuelve a ingresar el código, selecciona una opción diferente o vuelve a intentarlo.\n")