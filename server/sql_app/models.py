from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base
import datetime
from sqlalchemy.sql.sqltypes import DATETIME


class upload_file(Base):
    __tablename__="upload_file"
    id = Column(Integer,primary_key=True, autoincrement=True)
    create_date = Column(DATETIME, default=datetime.datetime.now, nullable=False)
    old_name = Column(String)
    new_name = Column(String)
    parent_id = Column(Integer)
    type = Column(String, nullable=True)
    