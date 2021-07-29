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
)

scraper = Scraper()

@app.get('/')
async def home():
    return "Colombia.com api scraper By Fabian"

@app.get('/movies')
async def getMovies():
    return scraper.getMovies()

@app.get('/movies/{id}')
async def getMovie(id: str):
    return scraper.getMovie(id)

@app.get('/movies/schedule/{city}/{id}')
async def getSchedule(city: str, id: str):
    return scraper.getMovieSchedule(city, id)