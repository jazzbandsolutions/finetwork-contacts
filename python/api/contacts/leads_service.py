import logging
from botocore.exceptions import ClientError
logger = logging.getLogger()
logger.setLevel(logging.INFO)
import requests


def createLead(data): 
    url = "https://gateway.finetwork.com/hubspot/crm/contacts/lead/create"
    
    # Asegúrate de que los datos contengan todos los campos requeridos
    required_fields = ['firstName', 'lastName', 'phone']
    for field in required_fields:
        if field not in data:
            return {"error": f"Missing required field: {field}"}
        
    # token = get_external_token()
    
    # if not token:
    #     return {"error": "Failed to retrieve token"}
    
    # headers = {
    #     "Authorization": f"Bearer {token}",
    #     "Content-Type": "application/json"
    # }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return {'message': 'Created contact'}
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
        return {"error": f"Other error occurred: {err}"}