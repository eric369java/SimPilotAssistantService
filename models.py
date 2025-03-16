import uuid as uuid_pkg
from sqlmodel import Field, SQLModel

class Aircraft(SQLModel, table=True):
    id: uuid_pkg.UUID = Field(default_factory=uuid_pkg.uuid4, primary_key=True)
    name: str
    type: str
    manufacturer: str

class Checklist_Item(SQLModel, table=True):
    id: uuid_pkg.UUID = Field(default_factory=uuid_pkg.uuid4, primary_key=True)
    aircraft_id : uuid_pkg.UUID = Field(nullable=False)
    item_order : int = Field(nullable=False, index=True)
    challenge : str = Field(nullable=False)
    answer : str = Field(nullable=False)
    condition : str | None
    procedure : str = Field(nullable=False)
    details : str | None
