# API REST para la Wiki del Juego

## Objetivo
El objetivo de esta práctica es realizar un prototipo como prueba de concepto antes de decidirse a migrar una base de datos relacional a una base de datos de documentos, específicamente MongoDB, para mejorar el rendimiento del sistema debido al alto volumen de jugadores. La API REST actual tiene diversos endpoints que proporcionan información sobre objetos del juego, monstruos, mazmorras, habitaciones, usuarios y comentarios. Además, se plantea extender la API para satisfacer las necesidades de otros equipos de la empresa, como Quality Assurance, PR y Marketing.

## Tareas realizadas
- Realizar consultas desde Python o MongoDB Compass para cada uno de los endpoints de la API REST.
- Crear una nueva colección para almacenar comentarios y sugerencias.
- Realizar consultas.

## Endpoints desde Python
Una vez montada la base de datos en MongoDB, se pueden probar todas las endpoints implementadas ejecutando `api_calls.ipynb`.
### GET
#### get_loot()
    Realiza una consulta a la base de datos para obtener los identificadores y nombres de todos los objetos loot, los cuales son devueltos en formato JSON y ordenados por su identificador de forma ascendente.

#### get_loot_by_id()
    Busca y devuelve información detallada sobre un objeto loot específico identificado por su id, incluyendo su nombre, cantidad de oro, tipos, peso y sus atributos de existencia en las habitaciones y mazmorras, en formato JSON.

#### get_monster()
    Realiza una consulta para obtener información básica sobre todos los monstruos del juego, incluyendo su id, nombre, nivel y tipo, ordenados por id y devueltos en formato JSON

#### get_monster_by_id()
    De la misma manera que las funciones implementadas para loot, esta busca y devuelve información detallada sobre un monstruo específico del juego identificado por su id, incluyendo su experiencia, nombre, tipo, nivel, página de manual y ubicaciones en las habitaciones y mazmorras, en formato JSON.

Estas siguientes funciones `GET` difieren a las anteriores, ya que los dungeons no tienen una colección propia, sino que se mencionan por id y nombre en las rooms. 

#### get_dungeon()
    Para la consulta se ha realizado lo siguiente: 

    1. Agrupar las habitaciones por dungeon_id y dungeon_name.
    2. Ordenar los resultados por dungeon_id en orden ascendente.
    3. Proyectar los campos _id.dungeon_id y _id.dungeon_name con nombres diferentes (idD y name).
    4. Devolver la información en JSON.

#### get_dungeon_by_id()
    Para resolver este problema, se han seguido estos pasos:

    1. Extraer todas las habitaciones (rooms) que pertenezcan al dungeon especificado.
    2. Recorrer cada una de estas habitaciones para obtener la información deseada (información de la habitación, count_of_comment_categories, monsters y loot). La información de las habitaciones, los monsters y loot son consultas básicas por room id, count_of_comment_categories se realiza encontrando la lista de hints de la room indicada, 'descombrimiendo' su info en un unwind, agrupando por catgoría y proyectando para tener el count por categoría.
    3. Se ha considerado que los hints de categoría "lore" representan la información de lore.

    Para una versión posterior:

    Dentro de la información requerida para el grafo interactivo, es probable que haya muchos objetos repetidos (loot, monstruos). Por lo tanto, optamos por devolver un contador de cada instancia de loot y monstruo junto con la información para que se puedan crear aristas en el grafo mencionando el número de instancias de estos objetos o para asignarles un peso.

Volvemos a consultas sencillas, similares a las primeras explicadas. 

#### get_room_by_id()
    Esta función trabaja como get_loot_by_id() y get_monster_by_id(), extrayendo la información de la habitación indicada por id.

#### get_user() 
    Busca y devuelve información básica sobre todos los usuarios del juego, incluyendo sus correos electrónicos (email), nombres de usuario (user_name) y países (country), ordenados alfabéticamente por correo electrónico, en formato JSON.

#### get_user_by_email()
    Busca y devuelve información detallada sobre un usuario específico del juego identificado por su correo electrónico (email). La información devuelta incluye el correo electrónico, nombre de usuario, país, fecha de creación del usuario y detalles de los comentarios realizados por el usuario, incluyendo la categoría del comentario, el texto, la fecha de creación y la referencia a la habitación y mazmorra asociadas, en formato JSON.

### POST
En estas endpoints se especifica la necesidad de autenticación, ya sea por parte del usuario o por el admin. Se planetaron dos soluciones: 
- Por parte del admin se creó un usuario en la base de datos, con su nombre y contraseña correspodiente, con las que se tendrá que realizar la conexión a la base de datos para las consultas, de esta forma pudiendo asegurar la conexión en caso de ser correctas y realizar los cambios en la base de datos.
- Para la autenticación de usuario se planteó por un lado lo comentado para el admin, y por otro lado la opción de realizar un comentario a través de su email y username, ya que dicha información es la única de la que disponemos de los usuarios que han accedido a la wiki. Si tuviéramos una base de datos con los login de los usuarios hubiésemos considerado simplemente realizar la autenticación con estos datos.

#### post_comment()
    Permite a un usuario autenticado añadir un comentario a una habitación específica del juego. Aquí está el flujo de la función:

    1. Se crea una conexión a la base de datos MongoDB y se verifica la autenticación.

    2. Se obtiene la información de la habitación (room_info) utilizando el room_id proporcionado para incluirla en los detalles del comentario.

    3. Se inserta un nuevo documento en la colección de usuarios (users) que contiene los detalles del comentario, incluyendo el correo electrónico del usuario, su nombre, la fecha de creación del comentario y la información de la habitación asociada.

    4. Se actualiza la habitación correspondiente en la colección de habitaciones (rooms) para añadir el nuevo comentario a la lista de comentarios de la habitación.
### post_monster()
    Permite a un administrador autenticado agregar un nuevo monstruo al juego.

    1. Se crea una conexión a la base de datos MongoDB y se verifica la autenticación.

    2. Se obtiene el último id de monstruo existente en la base de datos y se incrementa en uno para asignar el nuevo id al monstruo que se añadirá.

    3. Se inserta un nuevo documento en la colección de monstruos (monster) con los detalles del nuevo monstruo, incluyendo su nombre, tipo, nivel, ubicación, experiencia y página del manual.

    Dado que no se especificó quere mencionar las habitaciones en las que se encuentra el monstruo no se necesita ninguna actualización en otras colecciones.

    Este mismo procedimiento se realiza para `post_loot()`.
#### post_room()
    Dado que las rooms no tienen atributo dungeon_lore, y que anteriormente se ha considerado el lore de una dungeon como los hints de categoría lore de las rooms de la dungeon, hemos decidido añadir lore como un hint publicado por el admin de manera anónima para dar una descripción inicial de la dungeon.

    Permite a un administrador autenticado agregar una nueva habitación a una mazmorra específica en el juego.

    1. Se crea una conexión a la base de datos MongoDB y se verifica la autenticación.

    2. Se extrae información sobre las habitaciones conectadas (rooms_connected) a partir de los room_id proporcionados en la lista rooms_connected.

    3. Se asigna un nuevo room_id para la nueva habitación que se añadirá a partir del último room_id existente en la base de datos.

    4. Se inserta un nuevo documento en la colección de habitaciones (rooms) con los detalles de la nueva habitación, incluyendo su nombre, mazmorra asociada, habitaciones conectadas, puntos de entrada/salida y una pista inicial de lore.

    5. Se actualizan las habitaciones conectadas en la base de datos para incluir la nueva habitación en su lista de habitaciones conectadas.

### PUT
#### put_monsters_in_room()
    Permite actualizar la información de los monstruos presentes en una habitación específica del juego.

    1. Se obtiene información detallada sobre los monstruos proporcionados en una lista a partir de sus id correspondientes.

    2. Se actualiza la información de los monstruos en la habitación especificada en la colección de habitaciones (rooms), estableciendo la lista de monstruos presentes en la habitación.

    3. Se obtienen detalles adicionales sobre la habitación (nombre, mazmorra asociada) para actualizar la información de los monstruos en la colección de monstruos (monsters), agregando la habitación actual a la lista de habitaciones en las que se encuentran los monstruos.

    Se realiza lo mismo con la información correspondiente en put_loot_in_room().
#### put_rooms_connected_in_room()
    Permite actualizar la lista de habitaciones conectadas a una habitación específica del juego. 

    1. Se obtiene información detallada sobre las habitaciones conectadas proporcionadas en la lista rooms_connected a partir de sus room_id correspondientes.

    2. Se actualiza la información de las habitaciones conectadas en la habitación especificada en la colección de habitaciones (rooms), estableciendo la lista de habitaciones conectadas.

    3. Se obtiene el nombre de la habitación actual para actualizar la lista de habitaciones conectadas en las habitaciones conectadas, añadiendo la habitación actual a su lista de habitaciones conectadas.

### DELETE

#### delete_room_by_id()
    Permite eliminar una habitación específica del juego y actualizar otras colecciones que hacen referencia a ella. 

    1. Se elimina la habitación especificada de la colección de habitaciones (rooms) utilizando su room_id.

    2. Se actualiza las colección de users,monsters y loot, para eliminar cualquier referencia a la habitación eliminada.
#### delete_monster_by_id() y delete_loot_by_id()
    Realizan lo mismo que la función delete_room_by_id(), solo que actualizan sus referencias en rooms.
    
## Creación de nueva colección Hints

## Consultas 