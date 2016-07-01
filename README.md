Plataforma web paralela
===================

La fase II del proyecto de laboratorio de la asignatura Computación Paralela, para el período
2016-I, considera como base, el modelamiento, diseño e implementación realizado en la
fase I. Por tal motivo, esta fase final, comprende requerimientos adicionales, en el ámbito
de técnicas de gestión de imágenes, en la capacidad de cómputo de la plataforma de Clúster
paralelo de tipo homogéneo, como de las fuentes de acceso multiplataforma de la solución
final.

----------

Personas asociadas al proyecto
-------------
> - **Coordinador**: Felipe S. Canales Saavedra.
> - **Grupo**: Grupo curso, computación paralela semestre 1 - 2016.
> - **Profesor**: Oscar Magna Veloso.


Alcance del proyecto
-------------

Las técnicas a considerar, comprende, a lo menos, las siguientes, agrupadas según el alcance
de las mismas:

> **Técnicas:**

> - Realzado y filtrado
> - Mejoras.
> - Movimiento
> - Operaciones matemáticas

Instalación de dependencias
-------------

 **Instalación de web.py**:
```bash
$ [sudo] pip install web.py
```

**Instalación de OpenCV (más dependencias asociadas)**:
```bash
$ cd
$ wget https://github.com/milq/scripts-ubuntu-debian/blob/master/install-opencv.sh
$ [sudo] chdmod 777 install-opencv.sh
$ ./sh install-opencv.sh
```

**Nota**: Precaución en la linea 47 del script "install-opencv.sh", cambiar el número 4 por la cantidad de procesadores que tenga disponible en su computador


