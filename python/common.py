from fastapi import Depends, Request, status, HTTPException
import os

async def on_permissions(request: Request):
    api_key = request.headers.get('X-API-Key')
    # TODO CAMBIAR A PARAMETER STORE
    valid_api_key = os.environ.get('API_KEY')

    if api_key != valid_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Acceso denegado")