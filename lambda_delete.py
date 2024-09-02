import json
import boto3
from unittest.mock import MagicMock
import unittest

# Supongamos que tu función lambda_handler y otras funciones están en un módulo llamado `lambda_function`
from src.contacts.app import lambda_handler, delete_contact

class TestLambdaHandler(unittest.TestCase):

    def setUp(self):
        # Configura el mock para DynamoDB
        self.dynamodb_mock = MagicMock()
        self.table_mock = MagicMock()
        self.dynamodb_mock.Table.return_value = self.table_mock
        boto3.resource = MagicMock(return_value=self.dynamodb_mock)
        boto3.client = MagicMock()

    def test_delete_contact(self):
        # Simula la configuración de DynamoDB
        self.table_mock.delete_item.return_value = {}

        # Simula el evento DELETE
        event = {
            'routeKey': 'DELETE /contacts/{pk}',
            'pathParameters': {
                'pk': '12345'
            }
        }
        context = {}  # Puedes dejar esto vacío si no lo usas

        # Llama a la función lambda_handler
        response = lambda_handler(event, context)

        # Verifica los resultados
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(json.loads(response['body']), 'Deleted Client 12345')
        self.table_mock.delete_item.assert_called_once_with(Key={'Pk': '12345', 'Sk': 'Client'})

    def test_delete_contact_with_error(self):
        # Simula la configuración de DynamoDB para lanzar una excepción
        self.table_mock.delete_item.side_effect = KeyError

        # Simula el evento DELETE
        event = {
            'routeKey': 'DELETE /contacts/{pk}',
            'pathParameters': {
                'pk': '67890'
            }
        }
        context = {}  # Puedes dejar esto vacío si no lo usas

        # Llama a la función lambda_handler
        response = lambda_handler(event, context)

        # Verifica los resultados
        self.assertEqual(response['statusCode'], 400)
        self.assertEqual(json.loads(response['body']), 'error in delete contacts')
        self.table_mock.delete_item.assert_called_once_with(Key={'Pk': '67890', 'Sk': 'Client'})

if __name__ == '__main__':
    unittest.main()
