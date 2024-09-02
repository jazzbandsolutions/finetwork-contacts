from  src.contacts.app import lambda_handler
import json

event = {
    "routeKey": "GET /contacts"
}
# Intenta imprimir la función importada para asegurarte de que es una función
print(type(lambda_handler))

# Llama a la función lambda_handler con el evento simulado
response = lambda_handler(event, None)

print(response)