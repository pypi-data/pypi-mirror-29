=====
Usage
=====

To use TrapecioCompuesto in a project::

    trapecio(limite_inferior, limite_superior, subintervalos, expresion_polinomica)
    
    >>> from trapecio_compuesto.trapecio_compuesto import trapecio
    >>> trapecio(1.3, 1.8, 6, 'x**3 - 6*x**2 + 11*x - 6')

    Metodo trapecio compuesto
    x**3 - 6*x**2 + 11*x - 6

    puntos de corte
    [1.3, 1.3833333333333333, 1.4666666666666666, 1.5499999999999998, 1.633333333333333, 1.7166666666666663, 1.7999999999999996]

    valores reemplazados en f(x)
    [0.356999999999999, 0.382162037037038, 0.381629629629630, 0.358875000000001, 0.317370370370373, 0.260587962962965, 0.192000000000004]

    el resultado es:  0.164593750000001
