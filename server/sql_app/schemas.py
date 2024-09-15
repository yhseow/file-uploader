from pydantic import BaseModel
import datetime


class upload_file(BaseModel):
    id: int
    create_date: datetime.datetime
    old_name: str
    new_name: str
    parent_id: int
    type: str
    
    
    class Config:
        orm_mode = True
