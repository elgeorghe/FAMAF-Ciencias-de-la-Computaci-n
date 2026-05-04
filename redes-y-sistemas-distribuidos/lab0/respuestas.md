1. ¿Cómo sabe el cliente que terminó de recibir la respuesta?
El cliente llama a read_line(connection) en un bucle hasta que la línea leída sea b'\r\n' o b''  asi sabe que terminó la parte de headers cuando llega la linea en blanco que separa headers y body o cuando ya no hay mas datos
y luego para el body lee en un bucle con recv hasta que el servidor termine la conexion, recv devuelva b''

2. ¿Qué parte del comportamiento depende de TCP y cuál de HTTP?
del HTTP dependen:
    - el formato del mensaje
    - semantica del codigo de estado
    - formato del pedido
y del TCP:
    - que lleguen los bytes en orden
    - que recv devuelva datos hasta recibir b''
    - existencia de una conexion confiable entre el cliente y el servidor 

3. ¿Qué pasaría si el servidor no cerrara la conexión después de enviar la respuesta?
el bucle while data != b'' nunca se cumple por lo que el cliente queda esperando mas datos y si no hay un timeout configurado el archivo puede quedar incompleto o colgado

4. ¿Por qué la IP obtenida para el mismo hostname podría ser distinta entre ejecuciones (o entre máquinas)?
cada maquina tiene su propio cache DNS con tiempos de expiracion (TTL) lo que puede causar que una maquina tenga una ip "vieja" y tambien puede pasar que un mismo hostname puede tener varios registros A. El servidor DNS puede devolverlos en orden rotado o distinto en cada consulta

5. ¿Por qué DNS suele usar UDP y HTTP usa TCP? ¿Qué pasaría si usáramos TCP para las consultas DNS en este cliente? (opcional, profundización)
DNS suele usar UDP porque:
    - una consulta y respuesta generalmente es menor a 512 bytes
    - al no tener handshakes o cierre de conexion es mas rapido y con menos carga en servidores 
    - modelo natural de “pregunta–respuesta” sin mantener estado de conexión
HTTP usa TCP porque:
    - transfiere mas informacion
    - necesita mas fiabilidad din perdidas, duplicados y en orden
si este cliente usara TCP todavia se podria obtener la ip correcta pero habria que cambiar el socket y cada consulta seria mas lenta y con mas overhead