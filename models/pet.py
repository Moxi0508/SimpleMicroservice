from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field



class PetBase(BaseModel):
    """Base Pet model."""
    id: UUID = Field(
        default_factory=uuid4,
        description="The unique ID of the pet (can be server-generated or client-provided).",
        json_schema_extra={"example": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d"},
    )
    name: str = Field(
        ...,
        description="The pet's name.",
        json_schema_extra={"example": "Fido"},
    )
    species: str = Field(
        ...,
        description="The species of the pet (e.g., 'Dog', 'Cat', 'Hamster').",
        json_schema_extra={"example": "Dog"},
    )
    age: Optional[int] = Field(
        None,
        description="The age of the pet (optional).",
        json_schema_extra={"example": 3},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
                    "name": "Whiskers",
                    "species": "Cat",
                    "age": 2,
                }
            ]
        }
    }

class PetCreate(PetBase):
    """Creation payload; ID is generated server-side but present in the base model."""
    model_config = {
            "json_schema_extra": {
                "examples": [
                    {
                        "id": "11111111-1111-4111-8111-111111111111",
                        "name": "Buddy",
                        "species": "Dog",
                        "age": 4,
                    }
                ]
            }
        }

class PetUpdate(BaseModel):
        """Partial update for an existing pet. Pet ID is taken from the path, not the body."""
        name: Optional[str] = Field(
            None, description="The pet's name.", json_schema_extra={"example": "Charlie"}
        )
        species: Optional[str] = Field(
            None, description="The species of the pet.", json_schema_extra={"example": "Parrot"}
        )
        age: Optional[int] = Field(
            None, description="The age of the pet.", json_schema_extra={"example": 5}
        )

        model_config = {
            "json_schema_extra": {
                "examples": [
                    {"name": "Charlie", "species": "Parrot", "age": 5},
                    {"age": 6},
                ]
            }
        }

class PetRead(PetBase):
        """Model for reading pet information (with timestamps)."""
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
                        "id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
                        "name": "Whiskers",
                        "species": "Cat",
                        "age": 2,
                        "created_at": "2025-01-15T10:20:30Z",
                        "updated_at": "2025-01-16T12:00:00Z",
                    }
                ]
            }
        }