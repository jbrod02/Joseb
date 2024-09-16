import re
from collections import defaultdict

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
        for token_type, tokens in tokens_encontrados.items():
            tokens_string = ', '.join(tokens)
            print(f"=== {token_type} ===\n{tokens_string}\n")

if __name__ == "__main__":
    while True:
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
        
        analizador = AnalizadorLexico()
        tokens = analizador.analizar(codigo_fuente)
        analizador.imprimir_tokens(tokens)