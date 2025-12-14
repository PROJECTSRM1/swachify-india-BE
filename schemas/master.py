from pydantic import BaseModel

class MasterOut(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}
