import boto3
from boto3.dynamodb.conditions import Key
from src.contacts.app import delete_contact

dynamodb = boto3.Session(profile_name="211125561005_apser-TEMP-AdministratorAccess").resource('dynamodb', region_name='eu-west-1')
table = dynamodb.Table("Test_lambda_vero")  

def insert_test_item(pk):
    try:
        response = table.put_item(
            Item={
                'Pk': pk,
                'Sk': 'Client',
                "firstName": "Don",
                "lastName": "Lucho",
                "phone": "1234567890",
                "nif": "AB123456C",
                "email": "Don.Lucho@Test.com",
            }
        )
        return 'Inserted Test Item ' + pk
    except Exception as e:
        return str(e)

def get_item(pk):
    try:
        response = table.get_item(
            Key={'Pk': pk, 'Sk': 'Client'}
        )
        return response.get('Item', 'Item not found')
    except Exception as e:
        return str(e)

# Inserta un ítem de prueba
pk_to_delete = '74323204556b4149ba723049a2eb9003'
print(insert_test_item(pk_to_delete))

# Llama a la función delete_contact para eliminar el ítem
result = delete_contact(pk_to_delete)
print(result) 

# Verifica si el ítem fue eliminado
verification_result = get_item(pk_to_delete)
print(verification_result)  




