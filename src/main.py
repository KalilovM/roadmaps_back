from fastapi import FastAPI

from src.users import models as users_models
from src.database import engine

from src.auth.router import router as auth_router
from src.users.router import router as user_router

import uvicorn

users_models.Base.metadata.create_all(bind=engine)
# users_models.Base.metadata.drop_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
