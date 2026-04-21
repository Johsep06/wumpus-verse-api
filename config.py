from typing import List
import os


def get_allowed_origins() -> List[str]:
    """Retorna origens permitidas baseadas no ambiente"""
    env = os.getenv("ENVIRONMENT", "development")

    origins = [
        'https://wumpus-verse-frontend.vercel.app',
        'http://localhost:5173',
    ]

    vercel_url = os.getenv("VERCEL_URL")
    if vercel_url:
        origins.append(f"https://{vercel_url}")

    if env == "development":
        origins.extend([
            'http://localhost:3000',
            'http://127.0.0.1:5173',
            'http://127.0.0.1:3000',
        ])

    return origins
