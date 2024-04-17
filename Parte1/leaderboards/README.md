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
Debido a la naturaleza de Cassandra, nos hemos visto obligados a cambiar la estructura de las inserciones, necesitando incluir country, username y dungeon_name (para poder devolver los datos requeridos en las escrituras y realizar búsquedas más optimas pues country se encuentra dentro de la clave primaria). La idea de la tabla se basa en la primera lectura hall of fame, y para cubrir los requerimientos utilizará country (puesto que los ranking son locales) y dungeon_id como claves primarias para la distribución entre los nodos y time minutes como clustering key para ordenar los tiempos de forma descendente. La limitación de esta tabla es que es imposible obtener en una única query el top 5 juagdores de todas las dngeons de un país, por tanto hemos recurrido a una función de python que hará queries para todas las dungeon_id del país, devolviendo una respuesta en formato json como la descrita en los requerimientos.

Otra opción que se nos ocurró fue crear una tabla que solo contenga el top 5 para country y dungeon_id, pero la rechazamos porque requeriría un update tras casa inserción algo que par ainserciones a gran escala es ineficiente.

### user_stats
Esta tabla dado el email del usuario y la dungeon devolverá todas las partidas del usuario dentro de esa dungeon.
```
CREATE TABLE IF NOT EXISTS user_stats (
    email text,
    dungeon_id int,
    time_minutes int,
    date text,
    PRIMARY KEY ((email, dungeon_id), time_minutes))
    WITH CLUSTERING ORDER BY (time_minutes ASC);
```
Aquí hemos utilizado el email del usuario y la dungeon id como claves primarias de forma que cassandra organice su distribución, seguidamente, y dado que puede ser intereante, decidimos incluir una clustering key con el tiempo en minutos que el usuario tardó en completar la mazmorra, poniendo en primera posición lso tiempos más bajos. 

Para ajustar el output a los requerimientos, hemos decidido de nuevo utilizar una fucnión de python que genera el json con los resultados.

### top_horde
Esta tabla difiere un poco de las demás pues se basa en eventos y kills de monstruos por parte de los usuarios.
```
CREATE TABLE IF NOT EXISTS top_horde (
    country text,
    event_id int,
    email text,
    user_name text,
    monster_id int,
    kill_id int,
    PRIMARY KEY ((country, event_id), email, kill_id)
);
```
Debido a la naturaleza de Cassandra, nos hemos visto obligados a cambiar la estructura de las inserciones, necesitando incluir country, username y un kill_id, siendo esta última esencial para el funcionamineto objetivo. De nuevo y de forma similar a hall_of_fame, decidimos establecer como claves primarias country y event_id (siendo dungeon_id en el caso anterior). Las clustering key son el email del usuario y, aunque inicialmente parezca de poco uso, kill_id. Esto es porque detnro de una fucnión de python, se hará una query a la tabla haciendo un groupby por los atributos country, event_id e email, devolviendo un count de los elementos de cada grupo, esto será el n_kills de los requerimientos, y este métdo count solo funciona si kill_id se encuentra dentro de las claves (además, al usar las claves primarias contry y event_id, nos aseguramos que el groupby se ejecuta en un solo nodo, reduciendo los problemas de eficiencia que tiene Cassandra con este tipo de operaciones). Seguidamente se ordena por n_kills y se devuelve un json con los top K usuarios con más kills.

Inicialmente pensamos es establecer un atributo tipo counter llamado n_kills dentro de la tabla que hiciese un update sumando uno tras cada inserción en la fila correspondiente, pero esto daba muchos problemas de velocidad y las queries eran poco limpias y comprensibles, por tanto optamos por la versión actual.


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

EXTRA: en `cassandra_queries.ipynb` puedes probar las consultas sin acceder a streamlit.

## 3. Conclusiones

Cassandra puede ser ideal para muchos casos, pero para muchos otros más puede requerir el uso de aplicaciones externas, como es el caso. Operaciones más complejas como grouby, ordenaciones que deben tener en cuenta más atributos pueden ser difíciles de implementar.

Finalmente ningún diseño es perfecto, en nuestro caso hay bastante duplicación de datos, y, aunque la posibilidad de minimizar el número de tablas parece fácil teniendo en cuenta que existen user_stats y hall_of_fame, conlleva sacrificar velocidad debido a la elección de keys.