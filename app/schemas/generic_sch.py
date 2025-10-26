from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional

class GernericMessage(BaseModel):
    message: str

    model_config = ConfigDict(from_attributes=True)
