from  src.contacts.app import lambda_handler
import json

event = {
    "routeKey": "POST /contacts/lead/create",
    "headers": {
        "Content-Type": "application/json"
    },
    "body": json.dumps({
        "firstName": "John",
        "lastName": "Doe",
        "phone": "1234567890",
        "nif": "AB123456C",
        "email": "john.doe@example.com"
    })
}
# Intenta imprimir la función importada para asegurarte de que es una función
print(type(lambda_handler))

# Llama a la función lambda_handler con el evento simulado
response = lambda_handler(event, None)
print(response)