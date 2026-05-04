# Pruebas de endpoint

Se utilizaran los ejemplos provistos por catedra via canal de zulip:

## Crear usuario
* **COMANDO 1:** 
> `curl -s -X POST http://localhost:5000/usuarios \` \
  `-H "Content-Type: application/json" \` \
  `-d '{"nombre": "Messi"}' | python3 -m json.tool`
* **RESPUESTA 1:**
{
    "id": 1,
    "nombre": "Messi"
}

* **COMANDO 2:** 
> `curl -s http://localhost:5000/usuarios | python3 -m json.tool`
* **RESPUESTA 2:**
[
    {
        "id": 1,
        "nombre": "Messi"
    }
]

* **COMANDO 3:** 
> `curl -s http://localhost:5000/usuarios/1 | python3 -m json.tool`
* **RESPUESTA 3:**
{
    "id": 1,
    "nombre": "Messi"
}

* **COMANDO 4:** 
> `curl -s -X PUT http://localhost:5000/usuarios/1 \` \
  `-H "Content-Type: application/json" \` \
  `-d '{"nombre": "Lionel Messi"}' | python3 -m json.tool`
* **RESPUESTA 4:**
{
    "id": 1,
    "nombre": "Lionel Messi"
}

* **COMANDO 5:** 
> `curl -s -X DELETE http://localhost:5000/usuarios/1 | python3 -m json.tool`
* **RESPUESTA 5:**
{
    "mensaje": "Usuario eliminado correctamente"
}


* **COMANDO 6:** 
> `curl -s http://localhost:5000/usuarios/1 | python3 -m json.tool`
* **RESPUESTA 6:**
{
    "error": "id de usuario no encontrada"
}
