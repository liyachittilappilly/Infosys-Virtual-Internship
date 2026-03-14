from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.routers import auth, users


# ─────────────────────────────────────────────
#  Lifespan: create tables on startup
# ─────────────────────────────────────────────


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create all DB tables on startup if they don't exist."""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created / verified.")
    yield
    print("🛑 Application shutting down.")


# ─────────────────────────────────────────────
#  App Initialization
# ─────────────────────────────────────────────

app = FastAPI(
    title="🎙️ Speech Therapy API",
    description=(
        "A secure REST API for the Speech Therapy application. "
        "Provides JWT-based user authentication: registration, login, logout, "
        "and user profile access."
    ),
    version="1.0.0",
    contact={
        "name": "Speech Therapy Team",
    },
    lifespan=lifespan,
)

# ─────────────────────────────────────────────
#  CORS Middleware
# ─────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
#  Routers
# ─────────────────────────────────────────────

app.include_router(auth.router)
app.include_router(users.router)


# ─────────────────────────────────────────────
#  Root Health Check
# ─────────────────────────────────────────────


@app.get("/", tags=["Health"], summary="API Health Check")
def root():
    """Returns a simple health-check response."""
    return {
        "status": "ok",
        "message": "🎙️ Speech Therapy API is running!",
        "docs": "/docs",
    }
