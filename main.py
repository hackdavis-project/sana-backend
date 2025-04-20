from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os
from routes.auth import router as auth_router
from routes.communities import router as communities_router
from routes.journal import router as journal_router
from routes.resources import router as resources_router
from routes.tts import router as tts_router
from routes.comments import router as comments_router
from routes.spt import router as spt_router

from dotenv import load_dotenv

import uvicorn

load_dotenv()


def main():
    app = FastAPI()

    # Get frontend URL from environment or use default
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[frontend_url],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(
        SessionMiddleware,
        secret_key=os.getenv("SESSION_SECRET_KEY", "super-secret-key"),
        same_site="lax",
    )

    app.include_router(auth_router, prefix="/api")
    app.include_router(communities_router, prefix="/api")
    app.include_router(journal_router, prefix="/api")
    app.include_router(resources_router, prefix="/api")
    app.include_router(tts_router, prefix="/api")
    app.include_router(comments_router, prefix="/api")
    app.include_router(spt_router, prefix="/api")

    @app.get("/")
    async def root():
        return {"message": "success"}

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
