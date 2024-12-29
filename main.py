from fastapi import FastAPI

from api.route_user import router as user_router  # Make sure this is correct

app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["users"])




@app.get("/")
async def root():
    return{"My first FastAPI app"}