from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import endpoints

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://queryweb3.wmjtyd.net" ,"http://queryweb3.com","http://www.queryweb3.com", "https://queryweb3.com","https://www.queryweb3.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add routes
app.include_router(endpoints.router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Welcome to QueryWeb3 API"}
