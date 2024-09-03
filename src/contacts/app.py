import json
import uuid
import boto3
from boto3.dynamodb.conditions import Key
import logging

# Configura el logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
table = dynamodb.Table("Test_lambda_vero")  # Asegúrate de que este nombre sea correcto

def lambda_handler(event, context):
    print(event)
    body = {}
    statusCode = 200
    headers = {"Content-Type": "application/json"}

    # Obtener el token de autorización del encabezado
    auth_header = event.get('token', {})
    token = auth_header.split(' ')[1] if auth_header and ' ' in auth_header else None

    if not token or not verify_token(token):
        return {
            'statusCode': 401,
            'headers': headers,
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
    valid_tokens = ['token', 'another-valid-token']
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
