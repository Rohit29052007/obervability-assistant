from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Observability Assistant",
    description="Convert natural language to PromQL queries",
    version="1.0.0"
)

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include API routes
from app.api.endpoints import router
app.include_router(router)

@app.get("/")
async def root():
    return {
        "message": "Observability Assistant Backend",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": "/api/test"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)