# server.py: initialize components, load routes, start server

# === Environment & Config ===
from dotenv import load_dotenv
from loguru import logger
from contextlib import asynccontextmanager

# === FastAPI Imports ===
from fastapi import FastAPI

# === Local Imports ===
from config.settings import settings 

# === Load .env File ===
load_dotenv()

# === Optional: Nest AsyncIO for Notebooks or Development Tools ===
import nest_asyncio
nest_asyncio.apply()

# === Router Imports ===
# from apis.v1.intent_router import router as intent_router
# from apis.v1.chat_router import router as chat_router
# from apis.v1.meilisearch_router import router as meilisearch_router
# from apis.v1.demo_router import router as demo_router
from apis.v2.demo_router import router as demo_router_v2

# === Lifespan Event for Startup/Shutdown ===
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"🚀 Starting {settings.app_name}...")
    yield
    logger.info("🛑 Shutting down...")

# === Initialize FastAPI App ===
api_server = FastAPI(
    title=settings.app_name,
    description="Agriculture LLM-Powered API Demo",
    version="0.1.0",
    debug=settings.debug_mode,
    lifespan=lifespan
)

# === Health Check Endpoint ===
@api_server.get("/health")
def health_check():
    logger.info("Health check requested.")
    return {"status": "ok"}

# === Include Routers ===
# api_server.include_router(intent_router, prefix="/v1")
# api_server.include_router(chat_router, prefix="/v1")
# api_server.include_router(meilisearch_router, prefix="/v1")
# api_server.include_router(demo_router, prefix="/v1")
api_server.include_router(demo_router_v2, prefix="/v2")

# === Run the Server ===
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:api_server", host="0.0.0.0", port=8001, reload=True)
