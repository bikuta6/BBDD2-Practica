# Editor de Niveles Colaborativos para "The Jötun's Lair"

## Tabla de Contenidos

1. [Descripción](#descripción)
3. [Configuración del Entorno](#configuración-del-entorno)
4. [Consultas desde la Interfaz Web](#consultas-desde-la-interfaz-web)
5. [Consultas y visualizaciones desde Python](#consultas-visualizaciones-desde-python)

## Descripción

Este apartado del proyecto tiene como objetivo darle funcionalidad a la migación de la base de datos relacional a una base de datos basada en grafos. Se han diseñado consultas y funcionalidades tanto para la interfaz web como para Python.

## Configuración del Entorno

Una vez clonado el repositorio de GitHub, sigue estos pasos:

1. Abre la terminal y navega hasta la carpeta `Parte1/editor_niveles` utilizando el comando `cd`.
2. Verifica que tengas las siguientes carpetas en el directorio:
   - `data` (debe estar vacía)
   - `import` (debe contener el archivo `dungeons.dump`)
   - `plugins` (debe estar vacía)
   - `sources` (debe contener los archivos `queries.ipynb` y `visualization.ipynb`)
   - `startup` (debe contener el script `install_dependences.sh`)
3. Ejecuta el comando Docker que se encuentra en el archivo `docker_command.txt`.
4. Ejecuta el comando `docker-compose up -d`. Una vez que el servicio de Neo4j muestre en los logs 'Started.', podrás realizar consultas desde el navegador, probar las consultas a la base de datos con Jupyter o ejecutar nuestra interfaz de usuario.

Para montar la interfaz de usuario:

1. Navega hasta la carpeta `Parte1/user_interface` utilizando el comando `cd` en la terminal.
2. Instala las dependencias necesarias ejecutando `pip install -r requirements.txt`.
3. Ejecuta el comando `python main.py`.
4. Para finalizar la ejecución de la interfaz, presiona `Ctrl+C` en la terminal.

La interfaz de usuario facilita la prueba de las funciones implementadas en Python mencionadas en los apartados anteriores, incluyendo además las consultas programáticas del apartado 'leaderboards' de esta parte del proyecto. Consulta el [README](../leaderboards/README.md) para obtener más información sobre el apartado de Cassandra.

## Consultas desde la Interfaz Web

Después de configurar el entorno, puedes verificar la funcionalidad de las consultas disponibles en la carpeta `editor_niveles\queries`. Para probarlas, accede a la interfaz web de Neo4j en `localhost:7687`.

Las consultas disponibles son:

1. **Buscar Salas con Tesoros**: Encuentra todas las salas de todas las mazmorras que contienen un tesoro específico.
2. **Monstruos en una Sala**: Obtiene todos los monstruos presentes en una sala específica.
3. **Monstruos Ausentes**: Obtiene todos los monstruos que no están presentes en ninguna sala.
4. **Camino Más Corto**: Calcula el camino más corto de un área a otra.
5. **Enemigos en el Camino Más Corto**: Muestra los enemigos que deben ser derrotados para ir de un área a otra por el camino más corto.
6. **Crear Nueva Arista**: Agrega una nueva arista que conecta las áreas del juego.
7. **Mapa-Mundi del Juego**: Visualiza el mapa-mundi del juego con las áreas y sus conexiones.
8. **Atributo de Mazmorra en Habitaciones**: Agrega un atributo nuevo en las habitaciones que indica la mazmorra a la que pertenecen.


## Consultas y visualizaciones desde Python

Podrás comprobar la funcionalidad de las consultas y visualizaciones mencionadas a continuación  desde `localhost:8899` para probarlas desde jupyter notebook. La ejecución resultante de las visualizaciones las podrás ver en local abriendo los ficheros .html que tendrás disponibles en 
editor_niveles\sources una vez ejecutado el código. Además, para hacer estas funciones más accesibles, la puedes probar desde en la interfaz de usuario explicada en el apartado [Configuración del Entorno](#configuración-del-entorno).

Consultas en queries.ipynb:

9. **Total de Oro en una Mazmorra**: Calcular el total de oro de los tesoros en una mazmorra.
10. **Nivel Medio de Monstruos**: Calcular el nivel medio de los monstruos en una mazmorra.
11. **Número Medio de Pasillos**: Calcular el número medio de pasillos en las salas de una mazmorra.
12. **Monstruos de Mayor Nivel**: Buscar las salas que contienen los monstruos de más nivel en una mazmorra.
13. **Experiencia de Encuentros**: Calcular la experiencia total de cada encuentro en una mazmorra y ordenarlos de mayor a menor.
14. **Sala con Mayor Experiencia**: Encontrar la sala que contiene el encuentro con más experiencia en una mazmorra.

Para la recomendación de monstruos se han implementado dos funciones en Python:

1. **Consulta Cypher**: Realiza una consulta Cypher para buscar otros monstruos que coaparezcan en otras salas con los monstruos del encuentro.
2. **Plugin GDS**: Utiliza el plugin GDS para realizar una recomendación de 5 monstruos ordenados según su relevancia.

Visualizaciones en visualization.ipynb:

1. **Mapamundi**: Visualización de las áreas del juego y sus conexiones.
2. **Listado de Mazmorras**: Listado de mazmorras con sus áreas y conexiones.
3. **Mini-Mapa de Mazmorra**: Visualización detallada de una mazmorra con entradas, salidas, monstruos, tesoros y niveles de estos.
