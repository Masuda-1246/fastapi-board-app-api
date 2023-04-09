from fastapi import APIRouter, HTTPException
from fastapi import Request, Response, Depends
from fastapi.encoders import jsonable_encoder
from schemas import Board, BoardBody, SuccessMsg
from database import db_create_board, db_get_boards, db_get_single_board, db_update_board, db_delete_board
from starlette.status import HTTP_201_CREATED
from typing import List
from fastapi_csrf_protect import CsrfProtect


router = APIRouter()

@router.post("/api/board", response_model=Board)
async def create_board(request: Request, response: Response, data: BoardBody, csrf_protect: CsrfProtect = Depends()):
  board = jsonable_encoder(data)
  res = await db_create_board(board)
  response.status_code = HTTP_201_CREATED
  if res:
    return res
  raise HTTPException(status_code=404, detail="Create task failed")

@router.get("/api/board", response_model=List[Board])
async def get_boards(request: Request):
  res = await db_get_boards()
  return res

@router.get("/api/board/{id}", response_model=Board)
async def get_single_board(request: Request, response: Response, id: str):
  res = await db_get_single_board(id)
  if res:
    return res
  raise HTTPException(status_code=404, detail=f"Task of ID:{id} doesn't exist")

@router.put("/api/board/{id}", response_model=Board)
async def update_board(request: Request, response: Response, id: str, data: BoardBody, csrf_protect: CsrfProtect= Depends()):
  board = jsonable_encoder(data)
  res = await db_update_board(id, board)
  if res:
    return res
  raise HTTPException(status_code=404, detail="Update task failed")

@router.delete("/api/board/{id}", response_model=SuccessMsg)
async def delete_board(request: Request, response: Response, id: str, csrf_protect: CsrfProtect= Depends()):
  res = await db_delete_board(id)
  if res:
    return {"message": "Successfully deleted"}
  raise HTTPException(status_code=404, detail="Delete task failed")
