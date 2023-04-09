from typing import Optional
from pydantic import BaseModel
from decouple import config

class Board(BaseModel):
  id: str
  title: str
  description: str

class BoardBody(BaseModel):
  title: str
  description: str


class SuccessMsg(BaseModel):
  message: str

