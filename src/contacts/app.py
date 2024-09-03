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
    valid_tokens = ['valid-token', 'another-valid-token', 'IQoJb3JpZ2luX2VjEKL//////////wEaCWV1LXdlc3QtMSJIMEYCIQCWAdQVbk2Xe9XlzJV+wQrJ9EXRmT0b2UUXbpDa8RrNxwIhAOgQQ3fWy8z+n7r7oWtUedoFYpyEE0DYEqDHpyemsDF6KpgDCLv//////////wEQABoMMjExMTI1NTYxMDA1IgxYD+kJSr87SmNTMbEq7AK+DWhh0StDEvBOGkWog0NF1subOu08iv6t2igrhci3iE400CecIbmGESCQw7xGJvms2xL3bDXhIT4Hb6zeo/MYI4/YY4PJVbILjmLdXcizuGyovZroSRrMgqrLVvvio3dA5D6D5tTskmGToZZHziHyRS2mv6vlCKW4Gd5Lk4fIkN1LgZ4dx+OJdZMQ4/LeJns4zuOKCcH6TUciiKpih6NXBeaDLqHUqWn8G6/4tvKyGx10KaIo0eTvW34MdgkVgqYysfYkNdKvCkN+rISBH3bSjJgugaDOLgs+57Oyh+U2dvZbbGfGzArR3WmtptqZyWK4jNhaWBN1yYTNMJMMfDTxA6UAL72xrjW8j9+patZwftOEGiM44UVFQNpbX/jipha+OWuCAs9b4jzoJAZpuqFXS8DAb/o3MPV9A3uI6xBnm+IeilczMY8ReK1BiJBm0uOZTleKH5Vh5zotUI8k1WQ8o0/lr7+tcNBfh/TvMPi627YGOqUBxcdwX4nau7V7qgYCkpvYZxgy5L1368tXaJEF3VHVhiN09PEt4J98D6zh0rTS+hRtwyr4txLOtZnKFWQHHTbUgfVhQiJ6jrxk+iSvpX4RM1FeLcS92snEdlJiPheUYE+2y+q263plvrqNW3prkNoNc8FVuaXmUjLZVjrZGc3eMxhjh6je2Ut0/DI/E+1J/k/AUyH1N9LukRGCbL5Xk5c6q+5njc/q']
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
