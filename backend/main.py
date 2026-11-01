
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from routes.query_routes import router as query_router
from routes.pdf_routes import router as pdf_router
from routes.image_routes import router as image_router

app = FastAPI(title="NCERT AI Assistant")

app.mount(
    "/chat-images",
    StaticFiles(directory="data/chat_images"),
    name="chat-images"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pdf_router)
app.include_router(query_router)
app.include_router(image_router)


@app.get("/")
def home():
    return {"status": "running"}
