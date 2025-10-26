from pydantic import BaseModel, ConfigDict

class GenericMessage(BaseModel):
    message: str

    model_config = ConfigDict(from_attributes=True)
