from pydantic import BaseModel

class DepartementBase(BaseModel):
    dpt: str
    abreviation: str

class DepartementCreate(DepartementBase):
    pass

class DepartementRead(DepartementBase):
    id: int

    class Config:
        orm_mode = True
