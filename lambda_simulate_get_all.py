from src.contacts.app import lambda_handler
import json

# Configura el evento para simular una solicitud GET /contacts
event = {
    "routeKey": "GET /contacts",
    "headers": {
        "Content-Type": "application/json"
    },
    "body": json.dumps({})  # Para un GET, el cuerpo generalmente puede estar vacío
}

# Imprime el tipo de la función importada para asegurarte de que es una función
print(type(lambda_handler))  # Esto debería imprimir <class 'function'>

# Llama a la función lambda_handler con el evento simulado
response = lambda_handler(event, None)

# Imprime la respuesta de la función lambda_handler
print(response)
