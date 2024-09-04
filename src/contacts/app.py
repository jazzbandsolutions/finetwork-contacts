import json
import uuid
import boto3
from boto3.dynamodb.conditions import Key
import logging

# Configura el logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dynamodb = boto3.Session(profile_name="211125561005_apser-TEMP-AdministratorAccess").resource('dynamodb', region_name='eu-west-1')
table = dynamodb.Table("Test_lambda_vero")  # Asegúrate de que este nombre sea correcto

def lambda_handler(event, context):
    print(event)
    body = {}
    statusCode = 200
    headers = {"Content-Type": "application/json"}

    # Obtener el token de autorización del encabezado
    auth_header = event.get('headers', {}).get('Authorization', '')
    print(f"auth_header: {auth_header}")  # Imprime el valor del encabezado

    # Verifica el formato del encabezado y extrae el token
    if auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
    else:
        token = None

    print(f"Extracted token: {token}")  # Imprime el valor del token extraído

    # Verifica si el token es válido
    if not token or not verify_token(token):
        return {
            'statusCode': 401,
            'headers': {"Content-Type": "application/json"},
            'body': json.dumps({'error': 'Unauthorized'})
        }

    try:
        if event['routeKey'] == "DELETE /contacts/{pk}":
            pk = event['pathParameters']['pk']
            body = delete_contact(pk)
        elif event['routeKey'] == "POST /contacts/lead/create":
            requestJSON = json.loads(event['body'])
            body = post_contacts(requestJSON)
        elif event['routeKey'] == "GET /contacts/{pk}":
            pk = event['pathParameters']['pk']
            body = get_contact_by_PK(pk)
        elif event['routeKey'] == "GET /contacts/identificationdocument/{NIF}":
            nif = event['pathParameters']['NIF']
            body = get_contact_by_nif(nif)
        elif event['routeKey'] == "GET /contacts/phone/{MSISDN}":
            value = event['pathParameters']['MSISDN']
            body = get_contact_by_phone(value)
        elif event['routeKey'] == "GET /contacts":
            if "queryStringParameters" in event:
                email = event["queryStringParameters"]['email']
                body = get_contact_by_email(email)
            else:
                body = get_contacts()
        elif event['routeKey'] == "PUT /contacts":
            requestJSON = json.loads(event['body'])
            table.put_item(
                Item={
                    'Pk': requestJSON['pk'],
                    'Sk': requestJSON['sk'],
                    'firstName': requestJSON['firstName'],
                    'lastName': requestJSON['lastName'],
                    'phone': requestJSON['phone'],
                    'nif': requestJSON['nif'],
                    'email': requestJSON['email']
                })
            body = 'Put item ' + requestJSON['pk']
    except KeyError:
        statusCode = 400
        body = 'Unsupported route: ' + event['routeKey']
    except Exception as e:
        statusCode = 500
        body = str(e)

    return {
        "statusCode": statusCode,
        "headers": headers,
        "body": json.dumps(body)
    }

def verify_token(token):
    valid_tokens = ['valid-token', 'another-valid-token', 'IQoJb3JpZ2luX2VjEL3//////////wEaCWV1LXdlc3QtMSJIMEYCIQDtD/CBFS68WydJCEvA9mlOAPPlX5Mvjf4X5PiiifXVGwIhANlKJ8TZls7/+6ot1PETBc7Iwtmj1cbJmsmth9OiqhMGKpgDCNb//////////wEQABoMMjExMTI1NTYxMDA1Igz2TlETyorkBf1PVqIq7AKfLhMyyNpOHAMCo8jOWIczYP+Qo8ECwsQBgQD77N6kzGRlbU6L9QzgMblrUfHcsgYbLV3DMNDMrq6gXzu7Q8fugwhh+KWFM/OtD/UigJONjlGnQUM82+LMTL7agbTZ+xbpzx7L2fUe0SzQcDprw/Dqb+9ig6ddzDG+yNiDXWLmb/4C//6XZRg7xzqHx8lU/s4CBLVDDC12e/E166d/44Y5XKZAOKJPf3gw2EE1lfJFM8TtSPPFBsDj/ne043TPTerQZFXlbJ2SVCnJnLXJjG1RifjXaDaswCLfZwvG886eCkgMj3Hsgy5YCBfSqM7WgxXu4+DGoRM5SY3OSkD4V+WPJbdz9hdOcT5PFp2szmlfFrGmKERJp8jwwRZOzQLtwMiYU2vwdcb8F4zahfS2Dz7309/xpf50+3Vp55sYRE65g1q8xZy1O+l3Isexx1sfEKv4v5ZsuCuvrMHBCJ8PnHEkzWVooxbAhu+yec25MIum4bYGOqUBiQUCpjxe9vrWFROcHF20RTjPAqBNZ1AffPnExG+Yd9YVt1bCgbrhwoDz01Xb4tTOnCPoXrW1r3wunAkoUTTxoS1aLHIUzzWqZXjx7VLfpxHW2pGKaOqplKSN2hp0nNbiOvCY5YGW8V12sgbiLbqs5qEoXhA1bzNVGeMfsUTceEOVUdEFswOr1vBlZgxgNjVR0K91IUOSjEOxUsxycFoOxpixHdaf']
    return token in valid_tokens

def delete_contact(pk):
    try:
        table.delete_item(
            Key={'Pk': pk, 'Sk': 'Client'}
        )
        return 'Deleted Client ' + pk
    except Exception as e:
        return str(e)

def post_contacts(requestJSON):
    try:
        table.put_item(
            Item={
                'Pk': uuid.uuid4().hex,
                'Sk': 'Client',
                'firstName': requestJSON['firstName'],
                'lastName': requestJSON["lastName"],
                'phone': requestJSON["phone"],
                'nif': requestJSON["nif"],
                'email': requestJSON["email"]
            })
        return 'Created contact'
    except Exception as e:
        return str(e)

def get_contacts():
    try:
        response = table.scan()
        items = response.get("Items", [])
        return [{'pk': item['Pk'],
                 'firstName': item['firstName'],
                 'lastName': item['lastName'],
                 'phone': item['phone'],
                 'nif': item['nif'],
                 'email': item['email']} for item in items]
    except Exception as e:
        return str(e)

def get_contact_by_PK(pk):
    try:
        response = table.get_item(Key={'Pk': pk, 'Sk': 'Client'})
        item = response.get("Item", {})
        return [{'firstName': item.get('firstName', ''),
                 'lastName': item.get('lastName', ''),
                 'phone': item.get('phone', ''),
                 'nif': item.get('nif', ''),
                 'email': item.get('email', '')}]
    except Exception as e:
        return str(e)

def get_contact_by_nif(value):
    try:
        response = table.query(
            IndexName='nif-index',
            KeyConditionExpression=Key('nif').eq(value)
        )
        return response.get("Items", [])
    except Exception as e:
        return str(e)

def get_contact_by_phone(value):
    try:
        response = table.query(
            IndexName='phone-index',
            KeyConditionExpression=Key('phone').eq(value)
        )
        return response.get("Items", [])
    except Exception as e:
        return str(e)

def get_contact_by_email(value):
    try:
        response = table.query(
            IndexName='email-index',
            KeyConditionExpression=Key('email').eq(value)
        )
        return response.get("Items", [])
    except Exception as e:
        return str(e)
