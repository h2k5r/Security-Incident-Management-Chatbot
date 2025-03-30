from fastapi import FastAPI
from app.routes.alert_routes import router as alert_router

app = FastAPI(
    title="Security Incident Management Chatbot",
    description="API for automated security incident management",
    version="1.0.0"
)

# Include routers
app.include_router(alert_router, prefix="/api", tags=["alerts"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Automated Security Incident Management Chatbot"}
