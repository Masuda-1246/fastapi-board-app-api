from decouple import config
from typing import Union
import motor.motor_asyncio
from bson import ObjectId
# from fastapi import HTTPException
import asyncio

MONGO_API_KEY = config('MONGO_API_KEY')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_API_KEY)
client.get_io_loop = asyncio.get_event_loop

database = client.API_DB
collection_board = database.board
collection_user = database.user

def board_serializer(board) -> dict:
  return {
    "id": str(board["_id"]),
    "title":board["title"],
    "description":board["description"]
  }

def user_serializer(user) -> dict:
  return {
    "id":str(user["_id"]),
    "email": user["email"]
  }

async def db_create_board(data: dict) -> Union[dict, bool]:
  board = await collection_board.insert_one(data)
  new_board = await collection_board.find_one({"_id": board.inserted_id})
  if new_board:
    return board_serializer(new_board)
  return False

async def db_get_boards() -> list:
  boards = []
  for board in await collection_board.find().to_list(length=100):
    boards.append(board_serializer(board))
  return boards

async def db_get_single_board(id: str) -> Union[dict, bool]:
  board = await collection_board.find_one({"_id": ObjectId(id)})
  if board:
    return board_serializer(board)
  return False

async def db_update_board(id: str, data: dict) -> Union[dict, bool]:
  board = await collection_board.find_one({"_id": ObjectId(id)})
  print(data)
  if board:
    updated_board = await collection_board.update_one(
      {"_id": ObjectId(id)},
      {"$set":data}
    )
    if updated_board.modified_count > 0:
      new_board = await collection_board.find_one({"_id": ObjectId(id)})
      return board_serializer(new_board)
    return False

async def db_delete_board(id: str) -> bool:
  board = await collection_board.find_one({"_id": ObjectId(id)})
  if board:
    deleted_board = await collection_board.delete_one({"_id": ObjectId(id)})
    if deleted_board.deleted_count > 0:
      return True
  return False

