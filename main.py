from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.owner import OwnerCreate, OwnerRead, OwnerUpdate
from models.pet import PetCreate, PetRead, PetUpdate
from models.health import Health

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
owners: Dict[UUID, OwnerRead] = {}
pets: Dict[UUID, PetRead] = {}

app = FastAPI(
    title="Owner/Pet API",
    description="Demo FastAPI app using Pydantic v2 models for Owner and Pet",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Address endpoints
# -----------------------------------------------------------------------------

def make_health(echo: Optional[str], path_echo: Optional[str]=None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo
    )

@app.get("/health", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    # Works because path_echo is optional in the model
    return make_health(echo=echo, path_echo=None)

@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)

@app.post("/pets", response_model=PetRead, status_code=201)
def create_pet(pet: PetCreate):
    if pet.id in pets:
        raise HTTPException(status_code=400, detail="Address with this ID already exists")
    pets[pet.id] = PetRead(**pet.model_dump())
    return pets[pet.id]

@app.get("/pets", response_model=List[PetRead])
def list_pets(
    name: Optional[str] = Query(None, description="Filter by pet name"),
    species: Optional[str] = Query(None, description="Filter by species"),
    age: Optional[int] = Query(None, description="Filter by age"),
):
    results = list(pets.values())

    if name is not None:
        results = [p for p in results if p.name == name]
    if species is not None:
        results = [p for p in results if p.species == species]
    if age is not None:
        results = [p for p in results if p.age == age]

    return results

@app.get("/pets/{pet_id}", response_model=PetRead)
def get_pet(pet_id: UUID):
    if pet_id not in pets:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pets[pet_id]


@app.patch("/pets/{pet_id}", response_model=PetRead)
def update_pet(pet_id: UUID, update: PetUpdate):
    if pet_id not in pets:
        raise HTTPException(status_code=404, detail="Pet not found")
    stored = pets[pet_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    pets[pet_id] = PetRead(**stored)
    return pets[pet_id]

# -----------------------------------------------------------------------------
# Owner endpoints
# -----------------------------------------------------------------------------
@app.post("/owners", response_model=OwnerRead, status_code=201)
def create_owner(owner: OwnerCreate):
    owner_read = OwnerRead(**owner.model_dump())
    owners[owner_read.id] = owner_read
    return owner_read

@app.get("/owners", response_model=List[OwnerRead])
def list_owners(
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    phone: Optional[str] = Query(None, description="Filter by phone number"),
):
    results = list(owners.values())

    if first_name is not None:
        results = [o for o in results if o.first_name == first_name]
    if last_name is not None:
        results = [o for o in results if o.last_name == last_name]
    if email is not None:
        results = [o for o in results if o.email == email]
    if phone is not None:
        results = [o for o in results if o.phone == phone]


    return results
@app.get("/owners/{owner_id}", response_model=OwnerRead)
def get_owner(owner_id: UUID):
    if owner_id not in owners:
        raise HTTPException(status_code=404, detail="Owner not found")
    return owners[owner_id]

@app.patch("/owners/{owner_id}", response_model=OwnerRead)
def update_owner(owner_id: UUID, update: OwnerUpdate):
    if owner_id not in owners:
        raise HTTPException(status_code=404, detail="Owner not found")
    stored = owners[owner_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    owners[owner_id] = OwnerRead(**stored)
    return owners[owner_id]

# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Person/Address API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
