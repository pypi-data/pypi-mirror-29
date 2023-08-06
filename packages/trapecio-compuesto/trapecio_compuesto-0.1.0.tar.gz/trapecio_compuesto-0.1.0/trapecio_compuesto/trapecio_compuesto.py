# -*- coding: utf-8 -*-

"""Main module."""

from sympy import *
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application

def trapecio(a, b, n, entrada):
    """Función que evalua una expresión polinómica por el método del trapecio compuesto."""
    transformations = (standard_transformations + (implicit_multiplication_application,))
    x = symbols("x")

    print('Metodo trapecio compuesto')
    """entrada = input('expresion: ')
    a = float(input('ingrese el valor de a: '))
    b = float(input('Ingrese el valor de b: '))
    n = int(input('Ingrese el valor de n: '))"""

    h = (b-a)/n

    #expresiones = 0.2 + 25*(x) - 200*(x)**2 + 675*(x)**3 - 900*(x)**4 + 400*(x)**5
    expresiones = parse_expr(entrada, transformations=transformations)
    print(expresiones)
    intervalos = [a]
    sumados = 0
    fx = []

    for j in range(n):
        acumh = intervalos[j] + h
        intervalos.append(acumh)

    print('puntos de corte')
    print(intervalos)

    for j in range(n+1):
        funcion = expresiones.subs(x, intervalos[j])
        fx.append(funcion)

    print('valores reemplazados en f(x)')
    print(fx)

    for j in range(1, n):
        sumados += fx[j]

    i = (h/2)*(fx[0]+2*sumados+fx[n])
    print('el resultado es: ', i)
