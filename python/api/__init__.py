from fastapi import APIRouter, Depends
from .contacts.router import router as contacts

router = APIRouter(prefix="/api")

router.include_router(contacts, prefix="/contacts", tags=["contacts"])