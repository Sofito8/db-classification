

# Database classification

Proyecto de clasificación de información de bases de datos usando Django en docker.

La API permite cargar los parámetros de conexión de una base de datos, para posteriormente poder conectarse a ella y en base al nombre de las columnas de cada tabla las clasifica en tipos de información. Estos tipos de información pueden administrarse para personalizar la clasificación. Como resultado, se identifica toda la estructura de una base de datos, tablas y columnas, y el tipo de información almacenada en estas últimas.

El proyecto se desarrolló utilizando Docker Compose para permitir una compilación rápida del mismo. Se levantan tres containers:
- web:  aplicación en Django (Python).
- db: base de datos MySQL para la API.
- db-test: base de datos MySQL para realizar pruebas.

## Endpoints de la API:

- **GET** http://localhost:8000/api/v1/database/ 
Devuelve la información de conexión de todas las bases de datos cargadas
- **POST** http://localhost:8000/api/v1/database/
Permite almacenar la conexión de una base de datos siempre y cuando no se repitan. Body:
	>{
"host":"db-test",
"port":3307,
"username":"root",
"password":"rootpass"
}

- **GET** http://localhost:8000/api/v1/information_type/
Retorna todos los tipos de información empleados para clasificar las columnas de cada tabla
- **POST** http://localhost:8000/api/v1/information_type/
Permite agregar un nuevo tipo de información para ejecutar la clasificación, se le debe otorgar un nombre y la expresión regular a buscar:
	>{
"name":
"subString": 
}

- **DELETE** http://localhost:8000/api/v1/information_type/id/
En el caso de querer eliminar algun tipo de información, (as columnas anteriormentes clasificadas con este tipo se convierten en N/A).

- **GET** http://localhost:8000/api/v1/record/
Devuelve la información sobre todos los escaneos realizados, base de datos escaneada, fecha y si se realizó exitosamente

- **GET** http://localhost:8000/api/v1/database/scan/id/
Mediante una id asociada a la base de datos obtiene su estructura y clasificacion.
- **POST** http://localhost:8000/api/v1/database/scan/id/
Efectúa el escaneo de la base de datos indicada mediante el id.

## Bases de datos
A continuación se detallan los pasos para cargar ambas bases de datos mediante la terminal (Linux).
Por ejemplo descargamos la db en
   ```bash
   /home/system_db.sql
   ```
  1. Nos vamos a esa dirección
   ```bash
   cd /home/
   ```

2. Copiamos el archivo desde el árbol de directorio de nuestro usuario
   de Linux al arbol de directorios de del contenedor docker de la mysql.
   ```bash
   docker cp system_db.sql db:home/system_db.sql
   ```

3. Ahora accedemos al bash del container de la base de datos
   ```bash
   sudo docker exec -it db bash
   ```
   veremos lo siguiente:
   ```bash
   root@c70db16a259d:/#
   ```
   Nos movemos al direcorio donde guardamos el .sql
   ```bash
   cd /home/
   ```

4. Ejecutar el siguiente comando para importar la base de datos
   ```bash
   mysql -u root -p system_db < system_db.sql
   ```
   Ingresar la password ('rootpass'), enter.

Para la base de datos test repetir los pasos utilizando db-test como nombre de container y test_db como nombre de la base de datos.