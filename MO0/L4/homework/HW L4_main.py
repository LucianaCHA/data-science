'''

Uso de Módulos, Manejo de Excepciones y Logging

 Objetivo:  

Este ejercicio te permitirá aplicar conocimientos sobre el uso de módulos en Python, 
el manejo de excepciones, y el uso de logging para depurar y monitorear la ejecución 
de un programa.


1. Crea un módulo para cálculos matemáticos básicos:

*   En un archivo llamado calculadora.py, 
    define funciones para sumar, restar, multiplicar, y dividir dos números.
    
*   Asegúrate de incluir manejo de excepciones para la función de división, 
    capturando el caso de una división por cero e imprimiendo un mensaje de error.
'''


'''

En este archivo principal (main.py) utiliza el módulo calculadora:

*   Importa las funciones del módulo calculadora.py 

*   Crea un programa que solicite al usuario ingresar dos números y 
    una operación (sumar, restar, multiplicar, dividir).
    
*   Usa un bloque try-except para manejar posibles errores en la 
    entrada del usuario, como el ingreso de un valor no numérico.
'''

# importar modulo calculadora y sus funciones

from calculadora import sumar, restar, multiplicar, dividir

# Ingreso de valores (puedes usar la función input() para solicitar valores por teclado)
'''
Ejemplo
a = input("Ingrese un número")
print(a)
'''
try:
    a = input("Ingresa el primer número: ")
    b = input("Ingresa el segundo número: ")
    operacion = input("Elige una operación (sumar, restar, multiplicar, dividir): ")

    if operacion == "sumar":
        resultado = sumar(a, b)
    elif operacion == "restar":
        resultado = restar(a, b)
    elif operacion == "multiplicar":
        resultado = multiplicar(a, b)
    elif operacion == "dividir":
        resultado = dividir(a, b)
    else:
        print("Operación no válida.")
        resultado = None

    if resultado is not None:
        print(f"El resultado es: {resultado}")
except ValueError as e:
    print("Error: Entrada inválida. Debes ingresar números.")
