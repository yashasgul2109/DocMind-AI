from fastapi import FastAPI

from routes.query_routes import router as query_router

from routes.pdf_routes import router as pdf_router

app = FastAPI(title="NCERT AI Assistant")

app.include_router(pdf_router)
app.include_router(query_router)

@app.get("/")
def home():
    return {
        "status": "running"
    }