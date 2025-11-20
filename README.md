# Company News Finder

A simple application to find company news articles.

## How ir works

- Search for news articles about any company, filtered by time range
- Filters articles based on company name matches and industry keywords
- Shows relevance scores and reasons for each article
- Easy to use web interface

## Running it

Install packages:
```bash
pip install -r requirements.txt
```

Start server:
```bash
uvicorn app.main:app --reload
```

## Usage

Open http://localhost:8000 in your browser

Fill in company details, wait for it to finish. Click on completed job to see results. 

The UI updates job status automatically every few seconds.

## Structure

- `app/` - backend code
    - `main.py` - FastAPI app
    - `job_processor.py` - job processing logic
    - `utils.py` - helper functions
    - `config.py` - configuration constants
    - `models.py` - Pydantic models
    - `aggregators/` - news source aggregators - local articales from fixtures or real news APIs
    
- `static` - single page web UI
- `fixtures/` - sample news data 
- `data` - where results get saved individually per job
- `tests` - basic tests - unit and integration

## How scoring works

Articles get points for exact name matches, partial matches, and industry keywords. Only shows articles above a certain score.
- Exact name match: +20 points
- Partial name match: +2 points for each match, capped at max 10 points
- Industry keyword match: +2 points for each match, capped at max 10

