import os
from typing import List


class Settings:
    PROJECT_NAME: str = "AI Interior Designer Service"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",  # Vite frontend
        "http://127.0.0.1:5173",
        "http://localhost:5000",  # Node/Express backend
        "http://127.0.0.1:5000",
    ]


settings = Settings()

