legibilidad.py
==============

Basado en: https://github.com/amunozf/legibilidad/

Legibilidad, se refiere a la facilidad para leer un texto.

Este paquete realiza el cálculo en base a diversas fórmulas como:

- Fernández Huerta
- Gutiérrez
- Crawford
- Szigriszt-Pazos
- Inflesz
- Legibilidad µ

Instalación
-----------

    pip install legibilidad

Uso
---

.. code-block:: python

    from legibilidad import legibilidad
    texto = 'Legibilidad, se refiere a la facilidad para leer un texto'
    print(legibilidad.inflesz(legibilidad.szigriszt_pazos(texto)))

Más información
---------------

Recomiendo visitar el website del autor original: `legible.es <https://legible.es/>`_