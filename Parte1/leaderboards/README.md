# Objetivos



## 1. Planteamieto de la estructura

Tras observar la estructura de las tablas de la base de datos SQL y las queries ha realizar hemos planteado una solución de 3 tablas:

### hall_of_fame
Esta tabla es utilizada para obtener el top 5 de jugadores para cada mazmorra (en función del tiempo que se tardó en completar) para todas las mazmorras de un país. Optamos por la siguiente estructura:
```
CREATE TABLE IF NOT EXISTS hall_of_fame (
    country text,
    dungeon_id int,
    dungeon_name text,
    email text,
    user_name text,
    time_minutes int,
    date text,
    PRIMARY KEY ((country, dungeon_id), time_minutes))
    WITH CLUSTERING ORDER BY (time_minutes ASC);
```


## 2. Configuración del entorno

1. **Altera el fichero .sql**. Dentro de cada consulta de extracción de datos, en la línea ```INTO OUTFILE``` con la ruta de destino deseada, pues deberás mover estos archivos posteriormente. En nuestro caso es la de --secure-file-priv de mySQL Workbench.

2. **Mueve los .csv y el .cql a ./cluster/tmp/cassandra1**. Esto asegura que se encontrarán en /var/lib/cassandra/ en el contenedor.

3. **Inicia del clúster de Cassandra**. Utiliza el archivo `docker-compose.yml`
    proporcionado para iniciar tu clúster de Cassandra
4. **Verifica el estado del clúster**. Asegúrate de que todos los nodos
    estén funcionando correctamente mediante `nodetool` (quizá tarde un
    poco).
5. **Acceso a Cassandra**. Conéctate al clúster de Cassandra usando
    `cqlsh` a través del primer nodo.
6. **Ejecuta el archivo .cql**. Introduce en la línea de comandos:
```
SOURCE '/var/lib/cassandra/create_and_fill.cql'
```
Y espera a que haya terminado.

## 2. Creación de un Keyspace, Tablas e inserción de datos

1. **Creación de un _keyspace_**: Crea un keyspace llamado `bbdd2` con
    la estrategia de replicación `SimpleStrategy` y un factor de
    replicación de 3.
2. **Uso del _keyspace_**: Cambia al keyspace universidad para que todas
    las operaciones posteriores se realicen en este keyspace.
3. **Creación de una tabla**: Crea una tabla `estudiantes` con campos
    para el `id` del estudiante, `nombre`, `edad` y `carrera`.

## 3: Inserción y consulta de datos

1. **Carga de datos**: Carga los datos relativos a los estudiantes en la
    tabla `estudiantes`.
2. **Consulta de datos**: Realiza una consulta para verificar que la
    inserción se realizó correctamente.

## 4: Actualización y borrado de datos

1. **Actualización de datos**: Actualiza la edad de un estudiante.
2. **Borrado de datos**: Elimina un registro de estudiante.

## 5: Limpieza y finalización

1. **Borrado de la tabla**. Elimina la tabla `estudiantes`.
2. **Borrado del _keyspace_**. Elimina el keyspace `bbdd2`.
