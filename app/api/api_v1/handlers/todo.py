from fastapi import APIRouter, HTTPException, status, Depends

todo_router = APIRouter()

# Em java o código seria como abaixo:
# @RestController 
# @RequestMapping("/api/v1/todo")
@todo_router.get("/test")
async def test():
    return {"message": "Todo router is working!"}