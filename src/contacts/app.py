import json
import boto3
import uuid
from boto3.dynamodb.conditions import Key
# import requests

dynamodb = boto3.resource("dynamodb")
dynamodb_client = boto3.client("dynamodb")

TABLE = "Test_lambda_vero" #os.environ["TableContacts"]
table = dynamodb.Table(TABLE)

def lambda_handler(event, context):
    print(event)
    body = {}
    statusCode = 200
    headers = {"Content-Type": "application/json"}
    try:
        if event['routeKey'] == "DELETE /contacts/{pk}":
            pk= event['pathParameters']['pk']
            body = delete_contact(pk)
        elif event['routeKey'] == "POST /contacts/lead/create":
            requestJSON = json.loads(event['body'])
            body = post_contacts(requestJSON)
        elif event['routeKey'] == "GET /contacts/{pk}":
            pk = event['pathParameters']['pk']
            body = get_contact_by_PK(pk)
        elif event['routeKey'] == "GET /contacts/identificationdocument/{NIF}":
            nif= event['pathParameters']['NIF']
            body = get_contact_by_nif(nif)
        elif event['routeKey'] == "GET /contacts/phone/{MSISDN}":
            value= event['pathParameters']['MSISDN']
            body = get_contact_by_phone(value)
        elif event['routeKey'] == "GET /contacts":
            if 'pathParameters' in event and event['pathParameters'] is not None:
              email= event['pathParameters']['email']
              if email is not None:
                body = get_contact_by_email(email)
              else:
                body = get_contacts()
            else:
                body = get_contacts() 
        elif event['routeKey'] == "PUT /contacts":
            requestJSON = json.loads(event['body'])
            table.put_item(
                Item={
                    'Pk': requestJSON['pk'],
                    'Sk': requestJSON['sk'],
                    'firstName': requestJSON['firstName'],
                    'lastName': requestJSON["lastName"],
                    'phone': requestJSON["phone"],
                    'nif': requestJSON["nif"],
                    'email': requestJSON["email"]
                })
            body = 'Put item ' + requestJSON['pk']
    except KeyError:
        statusCode = 400
        body = 'Unsupported route: ' + event['routeKey']
    body = json.dumps(body)
    res = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body
    }
    return res

def get_contacts():
    try:
        body = table.scan()
        body = body["Items"]
        responseBody = []
        for items in body:
            responseItems = [
                    {'pk': items['Pk'],
                     'firstName': items['firstName'], 
                     'lastName': items['lastName'],
                     'phone': items['phone'],
                     'nif': items['nif'],
                     'email': items['email']}]
            responseBody.append(responseItems)
        body = responseBody
    except KeyError:
        body = 'error in get contacts'
    finally: 
        return body    

def get_contact_by_PK(pk):
    try:
        body = table.get_item(
                Key={'Pk': pk,
                     'Sk': 'Client'})
        body = body["Item"]
        responseBody = [
                {  'firstName': body['firstName'], 
                    'lastName': body['lastName'],
                    'phone': body['phone'],
                    'nif': body['nif'],
                    'email': body['email']}]
        body = responseBody
    except KeyError:
        body = 'error in get contact by Pk'
    finally: 
        return body    

def get_contact_by_nif(value):
    try:
        body = table.query(
                IndexName='nif-index',
                KeyConditionExpression=Key('nif').eq(value))
        body = body["Items"]
    except KeyError:
        body = 'error in get contact by nif'
    finally: 
        return body    

def get_contact_by_phone(value):
    try:
        body = table.query(
                IndexName='phone-index',
                KeyConditionExpression=Key('phone').eq(value))
        body = body["Items"]
    except KeyError:
        body = 'error in get contact by phone'
    finally: 
        return body    

def get_contact_by_email(value):
    try:
        body = table.query(
                IndexName='email-index',
                KeyConditionExpression=Key('email').eq(value))
        body = body["Items"]
    except KeyError:
        body = 'error in get contact by email'
    finally: 
        return body  

def post_contacts(requestJSON):
    try:
        table.put_item(
            Item={
                'Pk':uuid.uuid4().hex ,
                'Sk': 'Client',
                'firstName': requestJSON['firstName'],
                'lastName': requestJSON["lastName"],
                'phone': requestJSON["phone"],
                'nif': requestJSON["nif"],
                'email': requestJSON["email"]
                })
        return  'created contact'
    except KeyError:
        return 'error in get contacts'
    
def delete_contact(pk):
    try:    
        table.delete_item(
            Key={'Pk': pk,
                 'Sk': 'Client'})
        return  'Deleted Client ' + pk
    except KeyError:
        return 'error in delete contacts'