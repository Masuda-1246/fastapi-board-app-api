from fastapi import FastAPI
from routers import route_board
from schemas import SuccessMsg

app = FastAPI()
app.include_router(route_board.router)

@app.get("/",response_model=SuccessMsg)
def read_root():
  return {"message":"Welocome to Fast API"}