from fastapi import APIRouter, HTTPException, status, Depends

todo_router = APIRouter()

@todo_router.get("/test")
async def test():
    return {"message": "Todo router is working!"}