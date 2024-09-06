import logging
from botocore.exceptions import ClientError
logger = logging.getLogger()
logger.setLevel(logging.INFO)
import requests

def getContactByNif(nif):
    # token = get_external_token()
    # if not token:
    #     return {"error": "Failed to retrieve token"}
    
    url = f"https://gateway.finetwork.com/hubspot/crm/contacts/identificationdocument/{nif}"
    # headers = {
    #     "Authorization": f"Bearer {token}",
    #     "Content-Type": "application/json"
    # }

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
        return {"error": f"Other error occurred: {err}"}
    
    
def getContactByPhone(MSISDN):
    # token = get_external_token()
    # if not token:
    #     return {"error": "Failed to retrieve token"}
    
    url = f"https://gateway.finetwork.com/hubspot/crm/contacts/phone/{MSISDN}"
    # headers = {
    #     "Authorization": f"Bearer {token}",
    #     "Content-Type": "application/json"
    # }
    try:
        response = requests.get(url)
        response.raise_for_status()  # excepción si el código de estado no es 200
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
        return {"error": f"Other error occurred: {err}"}
    
def getContactByEmail(email):
    # token = get_external_token()
    # if not token:
    #     return {"error": "Failed to retrieve token"}
    
    url = f"https://gateway.finetwork.com/hubspot/crm/contacts/email/{email}"
    # headers = {
    #     "Authorization": f"Bearer {token}",
    #     "Content-Type": "application/json"
    # }

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
        return {"error": f"Other error occurred: {err}"}
