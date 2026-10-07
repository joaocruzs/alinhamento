from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.alignment_routes import router as alignment_router


app = FastAPI(
    title="DNA Sequence Alignment",
    description="Aplicação para alinhamento global e local de duas sequências de DNA.",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(alignment_router)


@app.get("/")
async def root():
    return {
        "application": "DNA Sequence Alignment",
        "version": "1.0.0",
        "status": "online"
    }


@app.get("/health")
async def health():
    return {
        "status": "ok"
    }