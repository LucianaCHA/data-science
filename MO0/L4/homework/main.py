
def main():
    # Importar el módulo calculadora
    from calculadora import sumar, restar, multiplicar, dividir

    # Ingreso de valores
    try:
        a = float(input("Ingresa el primer número: "))
        b = float(input("Ingresa el segundo número: "))
        operacion = input("Elige una operación \n"
        "S para sumar, R : restar,  M: multiplicar, D: dividir): ")

        if operacion == "S":
            resultado = sumar(a, b)
        elif operacion == "R":
            resultado = restar(a, b)
        elif operacion == "M":
            resultado = multiplicar(a, b)
        elif operacion == "D":
            resultado = dividir(a, b)
        else:
            print("Operación no válida.")
            resultado = None

        if resultado is not None:
            print(f"El resultado es: {resultado}")

    except ValueError:
        print("Error: Por favor ingresa números válidos.")

if __name__ == "__main__":
    main()