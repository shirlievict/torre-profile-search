from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# Allow CORS from any origin (frontend compatibility)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body model for /api/search
class SearchRequest(BaseModel):
    name: str

@app.post("/api/search")
async def search_profiles(request_data: SearchRequest):
    """
    Searches Torre profiles by name using the official Torre search endpoint.
    """
    torre_url = 'https://torre.ai/api/entities/_searchStream'
    body = {
        "query": {
            "term": {
                "name": request_data.name
            }
        }
    }

    try:
        response = requests.post(torre_url, json=body, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/genome/{username}")
async def get_genome(username: str):
    """
    Fetches detailed profile information (genome) of a given user.
    """
    try:
        response = requests.get(f'https://torre.ai/api/genome/bios/{username}')
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))