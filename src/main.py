from fastapi import FastAPI

from src.users import models as users_models
from src.database import engine

from src.auth.router import router as auth_router
from src.users.router import router as user_router
from src.config import API_VERSION_1

import uvicorn

users_models.Base.metadata.create_all(bind=engine)
# users_models.Base.metadata.drop_all(bind=engine)

app = FastAPI()

prefix = f"/api/{API_VERSION_1}"

app.include_router(auth_router, prefix=prefix)
app.include_router(user_router, prefix=prefix)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
