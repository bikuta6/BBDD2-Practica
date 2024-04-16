Comandos:

Una vez clonado el repositorio de github:

1. cd Parte1/editor_niveles
2. asegurarse de tener las siguientes carpetas:
    - data (vacía)
    - import (dungeons.dump)
    - plugins (vacía)
    - sources (queries.ipynb y visualization.ipynb)
    - startup (install_dependences.sh)
2. ejecutar comando docker de archivo docker_command.txt
3. docker compose up -d . Una vez el servicio de neo4j tiene en logs 'Started.' podremos realizar nuestras consultas desde el browser, probar queries a la base de datos con jupyter o montar nuestra user_interface.

Para montar el user_interface:
1. cd Parte1/user_interface
2. pip install -r requirements.txt
3. python main.py
4. en caso de querer finalizar la ejecución de la interfaz, ctrl+c en la terminal