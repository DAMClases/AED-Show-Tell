# AED-Show-Tell
Proyecto de AED con Backend Python | BBDD Documental MongoDB | Frontend Flet

# Documentación oficial

## Instalación de dependencias 
Para la gestión de paquetes y entornos virtuales, este proyecto utiliza Poetry. Esta herramienta nos permite asegurar que todos los desarrolladores utilicen exactamente las mismas versiones de las librerías, evitando el clásico problema de "en mi máquina funciona".

Si aún no tienes poetry instalado, sugerimos el siguiente comando en la terminal de VSC:

```
pip install poetry
```

Una vez clonado el repositorio, sitúate en la raíz del proyecto (donde se encuentra el archivo pyproject.toml) y ejecuta:

```
poetry install
```

Para lanzar la aplicación utilizando el entorno virtual configurado, utiliza el comando:

```
poetry run python main.py
```
Alternativamente, puedes activar la shell del entorno virtual para ejecutar comandos directamente:
```
poetry shell
python main.py
```

## Explicación del proyecto

Show & Tell es una academia privada que se dedica a la enseñanza no reglada en contextos educativos. Para la simulación de esta práctica hemos inventado las siguientes necesidades de la empresa con el fin de crear un programa que solvente y automatice los procesos empresariales, mejorando así la gestión de archivos y datos:

* La institución cuenta con tres usuarios: Administradores, docentes y alumnos.
* Los administradores pueden realizar las siguientes gestiones:
  1. Pueden gestionar y crear matrículas de alumnos: existen tres estados de matrícula (pendiente, pagado y cancelado).
  2. Pueden visualizar, editar, eliminar y crear nuevos cursos.
  3. Pueden visualizar, editar, eliminar y crear nuevos docentes.
  4. Pueden visualizar, editar, eliminar y crear nuevos alumnos.
  6. Pueden consultar su propia información de usuario.

En este sentido, el administrador actúa como el usuario con todos los privilegios sobre los datos. Puede realizar cualquier gestión dentro del modelo de negocio.
* Los docentes pueden realizar las siguientes gestiones:
1. Pueden visualizar, editar y crear nuevos cursos para impartir.
2. Pueden visualizar y consultar la información personal de cada alumno que está adscrito a un curso de éstos.

Los docentes tienen privilegios sobre las colecciones de datos referentes a cursos y docentes, y en menor medida pueden acceder a la información de los alumnos.

* Los alumnos pueden realizar las siguientes gestiones:
1. Pueden ver información de los cursos adscritos.
2. Pueden ver un resumen (dashboard) de cuantos cursos hay disponibles en la plataforma y en cuántos están apuntados.

* El principal problema de la institución era la incapacidad de informatizar profesionalmente los datos. Los datos estaban desperdigados en ficheros físicos y a menudo había un desfase documental y deterioro de información por pérdidas.

## Tecnologías, técnicas y métodos empleados para el desarrollo
Para solventar el problema de la empresa, hemos tenido que dividir las tareas de arquitectura de software en varias capas:

* La capa del backend: En la capa del backend, hemos decidido utilizar MongoDB como base de datos documental, teniendo en cuenta la flexibilidad y la facilidad para trabajar con los datos al romperse el esquema tradicional relacional. Para el driver o controlador, hemos utilizado PyMongo, un módulo de Python que permite la conexión y ejecución de consultas en la base de datos de MongoDB.

Desde el backend hemos controlado:

1. La conexión con la base de datos.
2. Las operaciones CRUD necesarias para establecer un pipeline eficaz con la capa del frontend.

* La capa del frontend: En la capa del frontend, hemos decidido utilizar Flet como framework para el desarrollo de una interfaz simple, elegante y moderna. Hemos pensado en todo momento en la escalabilidad, diseñando componentes reutilizables (layouts, cuadros de diálogo, dashboards...). El usuario es una parte fundamental, y por ello hemos implementado gráficos llamativos, accesibles y usables.

Desde la capa de frontend se renderiza la información solicitada y procesada por el backend.

Hemos pensado también en una estructura de directorios armoniosa, separando componentes en carpetas dedicadas. 
