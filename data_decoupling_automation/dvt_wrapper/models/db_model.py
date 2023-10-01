"""
This file will be used for validating the request payload
"""

from pydantic import BaseModel


class DataBase(BaseModel):
    """
    This DataBase Model will be used under the SourceTargetPayload model of request_model file
    which could be sent by End-User to validate schema designed.
    """

    db_type: str
    db_host: str
    db_name: str
    db_port: int
    db_user: str
    db_password: str


class ConnectionRequest(BaseModel):
    """
    The ConnectionRequest will be used to for the Source and Target Connection String for DVT-System as per DVT payload.
    """

    source_type: str
    host: str
    port: int
    user: str
    password: str
    database: str
