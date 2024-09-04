from src.contacts.app import lambda_handler
import json

# Configura el evento para simular una solicitud GET /contacts
test_token = "IQoJb3JpZ2luX2VjEL3//////////wEaCWV1LXdlc3QtMSJIMEYCIQDtD/CBFS68WydJCEvA9mlOAPPlX5Mvjf4X5PiiifXVGwIhANlKJ8TZls7/+6ot1PETBc7Iwtmj1cbJmsmth9OiqhMGKpgDCNb//////////wEQABoMMjExMTI1NTYxMDA1Igz2TlETyorkBf1PVqIq7AKfLhMyyNpOHAMCo8jOWIczYP+Qo8ECwsQBgQD77N6kzGRlbU6L9QzgMblrUfHcsgYbLV3DMNDMrq6gXzu7Q8fugwhh+KWFM/OtD/UigJONjlGnQUM82+LMTL7agbTZ+xbpzx7L2fUe0SzQcDprw/Dqb+9ig6ddzDG+yNiDXWLmb/4C//6XZRg7xzqHx8lU/s4CBLVDDC12e/E166d/44Y5XKZAOKJPf3gw2EE1lfJFM8TtSPPFBsDj/ne043TPTerQZFXlbJ2SVCnJnLXJjG1RifjXaDaswCLfZwvG886eCkgMj3Hsgy5YCBfSqM7WgxXu4+DGoRM5SY3OSkD4V+WPJbdz9hdOcT5PFp2szmlfFrGmKERJp8jwwRZOzQLtwMiYU2vwdcb8F4zahfS2Dz7309/xpf50+3Vp55sYRE65g1q8xZy1O+l3Isexx1sfEKv4v5ZsuCuvrMHBCJ8PnHEkzWVooxbAhu+yec25MIum4bYGOqUBiQUCpjxe9vrWFROcHF20RTjPAqBNZ1AffPnExG+Yd9YVt1bCgbrhwoDz01Xb4tTOnCPoXrW1r3wunAkoUTTxoS1aLHIUzzWqZXjx7VLfpxHW2pGKaOqplKSN2hp0nNbiOvCY5YGW8V12sgbiLbqs5qEoXhA1bzNVGeMfsUTceEOVUdEFswOr1vBlZgxgNjVR0K91IUOSjEOxUsxycFoOxpixHdaf"
event = {
    "routeKey": "GET /contacts/identificationdocument/{NIF}",
    "headers": {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {test_token}"
    },
    "pathParameters": {
            "NIF": "AB123456C"
    }
}

# Imprime el tipo de la función importada para asegurarte de que es una función
print(type(lambda_handler))  # Esto debería imprimir <class 'function'>

# Llama a la función lambda_handler con el evento simulado
response = lambda_handler(event, None)

# Imprime la respuesta de la función lambda_handler
print(response)