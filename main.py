from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scraper import Scraper

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["Content-Type"],
)

scraper = Scraper()

@app.get('/')
async def home():
    return "Colombia.com api scraper By Fabian"

@app.get('/movies')
async def movies():
    return scraper.GetMoviesSchedule()
