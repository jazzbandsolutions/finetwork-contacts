import json
from src.contacts.app import lambda_handler

event = {
    "routeKey": "POST /contacts/lead/create",
    "body": json.dumps({
        "firstName": "Don",
        "lastName": "Lucho",
        "phone": "1234567890",
        "nif": "AB123456C",
        "email": "Don.Lucho@Test.com"
    })
}
response = lambda_handler(event, None)
print(response)
