from pydantic import BaseModel
from typing import List

class BulkSessionCreate(BaseModel):
    roll_nos: List[str]
