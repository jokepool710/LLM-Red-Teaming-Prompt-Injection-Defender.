from fastapi import FastAPI
from routers import ai, threats

app = FastAPI(title="AI-Powered Cyber Threat Detection")

app.include_router(ai.router)
app.include_router(threats.router)

@app.get("/")
def root():
    return
