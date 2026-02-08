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

El aplicativo se descompone en **tres vistas**: una para el **administrador**, una para el **docente** y otra para el **alumno**. En cada una de las vistas las funciones se redistribuyen a favor del rol de cada usuario. Por ejemplo, en la vista del administrador se puede acceder a toda la lógica de negocio de la institución, pudiendo gestionar operaciones CRUD íntegras sobre todas las colecciones de datos. En cambio, en la vista del alumno, prácticamente solo puede efectuar operaciones de lectura sobre sus propios datos de cursos en los que está apuntado y su propia información personal, aportando verosimilitud a los requerimientos de la empresa ficticia.

Desde la capa de frontend se renderiza la información solicitada y procesada por el backend.

Hemos pensado también en una estructura de directorios armoniosa, separando componentes en carpetas dedicadas. 

## Colecciones y documentos

MongoDB organiza la información en documentos agrupados dentro de colecciones, y las colecciones viven dentro de una base de datos.

En este sentido, podemos simplificar con:
* Una base de datos contiene colecciones.
* Una colección es un grupo de documentos.
* Un documento es un objeto con estructura JSON pero que internamente se guarda como un BSON.

Tal y como hemos mencionado anteriormente en la documentación, este tipo de base de datos no es relacional. Los documentos no tienen por qué tener exactamente los mismos campos (ganando mucho en cuanto a flexibilidad) e incluso pueden presentar estructuras anidadas para modelar relaciones jerárquicas. 

Al presentar un esquema flexible, podemos ganar mucho más a la hora de cambiar el enfoque de nuestro aplicativo en futuros cambios y actualizaciones. 

Además, con la potencia de una base de datos no relacional podemos evitar reconstruir vistas con JOIN, simplemente trayendo en una sola consulta toda la colección y embebiendo en un procesado manual todos los datos que se necesiten, ahorrando múltiples lecturas. 

A continuación se exponen las diferentes colecciones que intervienen en el programa y que conforman la base de datos del aplicativo:

### Colección admin

Recoge los campos _id, nombre, apellidos, telefono, email, direccion y password. Esta colección aporta los datos personales para configuración de cuenta e inicio de sesión en la capa del administrador.

```
[{
  "_id": "admin_001",
  "nombre": "Cristopher",
  "apellidos": "Mendez Cervantes",
  "telefono": "612345678",
  "email": "cristophermc@gmail.com",
  "direccion": "Calle Mayor 12, Madrid",
  "password":"password"
},...
]
```
### Colección docentes

Recoge los campos _id, nombre, apellidos, telefono, email, direccion, cursos, estado, fecha_alta y password. Esta colección aporta los datos personales para configuración de cuenta, operaciones CRUD e inicio de sesión en la capa del docente. Además, tal y como se puede observar, el campo cursos tiene una anidación interna que relaciona directamente a un curso con un docente mediante los campos curso_id y titulo. 

```
[{
  "_id": "docente_001",
  "nombre": "Juan",
  "apellidos": "Jiménez García",
  "telefono": "612345678",
  "email": "jujimgardocente001@shndtel.com",
  "direccion": "Calle Mayor 12, Madrid",
  "cursos": [
    { "curso_id": "curso_001", "titulo": "Introducción a Java" },
    { "curso_id": "curso_002", "titulo": "Programación Orientada a Objetos" }
  ],
  "estado": "Alta",
  "fecha_alta": "2025-05-02",
  "password":"password"
},...
]
```

### Colección alumnos

Recoge los campos _id, nombre, apellidos, telefono, email, direccion, estado, fecha_alta, cursos, y password. Esta colección aporta los datos personales para configuración de cuenta, operaciones CRUD e inicio de sesión en la capa del alumno. Además, tal y como se puede observar, el campo cursos tiene una anidación interna que relaciona directamente a uno o varios cursos con un alumno mediante los campos curso, fecha_matricula y estado.

```
[{
  "_id": "alumno_001",
  "nombre": "Ana",
  "apellidos": "López Martín",
  "telefono": "698745632",
  "email": "anlopalumno001@shndtel.com",
  "direccion": "Av. del Sol 45, Valencia",
  "estado": "alta",
  "fecha_alta": "2025-09-01",
  "password":"password",
  "cursos" : [{"curso":"curso_001", "fecha_matricula":"27/03/2025", "estado":"pendiente"}]
  },...
]
```

### Colección cursos

Recoge los campos _id, titulo, descripcion, duracion_horas, precio e instructor. Esta colección aporta los datos necesarios para identificar los cursos que hay, qué cursos tiene asignado qué docente y aporta la capacidad realista de que los alumnos puedan tener cursos asignados en su colección. Además, tal y como se puede observar, el campo instructor tiene una anidación interna que relaciona directamente a un docente asignado mediante los campos docente_id y nombre.

```
[{
  "_id": "curso_001",
  "titulo": "Introducción a Java",
  "descripcion": "Curso básico para aprender los fundamentos del lenguaje Java.",
  "duracion_horas": 40,
  "precio": 34.99,
  "instructor": {
      "docente_id": "docente_001",
      "nombre": "Juan Jiménez García"
    }
},...
]
```
## Vistas

Tal y como se había explicado en la capa del frontend, tenemos 3 vistas principales en nuestro aplicativo:


En resumidas cuentas, utilizamos cuantro colecciones para dar vida a nuestra aplicación, bastando así para poder realizar las operaciones esenciales descritas en el epígrafe "Explicación del proyecto". 
