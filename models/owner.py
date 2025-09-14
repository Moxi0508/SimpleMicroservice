# file: owner.py
from __future__ import annotations

from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

# Key: Import PetBase from our new file
from .pet import PetBase

class OwnerBase(BaseModel):
    """Base Owner model."""
    first_name: str = Field(
        ...,
        description="The owner's given name.",
        json_schema_extra={"example": "John"},
    )
    last_name: str = Field(
        ...,
        description="The owner's family name.",
        json_schema_extra={"example": "Doe"},
    )
    email: EmailStr = Field(
        ...,
        description="The owner's primary email address.",
        json_schema_extra={"example": "john.doe@example.com"},
    )
    phone: Optional[str] = Field(
        None,
        description="The owner's contact phone number.",
        json_schema_extra={"example": "+1-555-123-4567"},
    )

    # Directly include the list of pets here, just as PersonBase included AddressBase
    pets: List[PetBase] = Field(
        default_factory=list,
        description="A list of pets belonging to this owner.",
         json_schema_extra={
             "example": [
                 {
                    "id": "e4a3b2c1-d0f9-4e8d-7c6b-5a4f3e2d1c0b",
                    "name": "Snowball",
                    "species": "Rabbit",
                    "age": 1,
            }
        ]
         },
    )

model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "first_name": "Jane",
                    "last_name": "Smith",
                    "email": "jane.smith@example.com",
                    "phone": "+1-555-789-1011",
                    "pets": [
                        {
                            "id": "e4a3b2c1-d0f9-4e8d-7c6b-5a4f3e2d1c0b",
                            "name": "Snowball",
                            "species": "Rabbit",
                            "age": 1,
                        }
                    ],
                }
            ]
        }
    }


class OwnerCreate(OwnerBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "first_name": "Jane",
                    "last_name": "Smith",
                    "email": "jane.smith@example.com",
                    "phone": "+1-555-789-1011",
                    "pets": [
                        {
                            "id": "e4a3b2c1-d0f9-4e8d-7c6b-5a4f3e2d1c0b",
                            "name": "Snowball",
                            "species": "Rabbit",
                            "age": 1,
                        }
                    ],
                }
            ]
        }
    }

class OwnerUpdate(BaseModel):
    first_name: Optional[str] = Field(None, json_schema_extra={"example": "Jonathan"})
    last_name: Optional[str] = Field(None, json_schema_extra={"example": "Davis"})
    email: Optional[EmailStr] = Field(None, json_schema_extra={"example": "jdavis@example.com"})
    phone: Optional[str] = Field(None, json_schema_extra={"example": "+1-555-444-3322"})
    pets: Optional[List[PetBase]] = Field(
        None,
        description="Provide a completely new list of pets to replace the old one.",
        json_schema_extra={
        "example": [
        {
            "id": "e4a3b2c1-d0f9-4e8d-7c6b-5a4f3e2d1c0b",
            "name": "Snowball",
            "species": "Rabbit",
            "age": 1,
        }
        ]
        },
    )

# In owner.py

class OwnerRead(OwnerBase):
    """Server representation of an Owner returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Owner ID.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "99999999-9999-4999-8999-999999999999",
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john.doe@example.com",
                    "phone": "+1-555-123-4567",
                    "pets": [
                        {
                            "id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
                            "name": "Fido",
                            "species": "Dog",
                            "age": 3
                        }
                    ],
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }