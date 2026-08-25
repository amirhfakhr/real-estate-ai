from fastapi import FastAPI
from schemas import SearchRequest
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://amirhfakhr.github.io"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return{"The API is running ... "}

@app.post("/search")
def search(data: SearchRequest):
    print(data)
    return{
        "message": "Search request received",
        "data":data
    }