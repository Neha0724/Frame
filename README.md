# Frame — Anime Data Studio

A full-stack anime analytics project using **React + Tailwind CSS**, **Flask REST API**, **Apache Spark**, and a **Random Forest rating predictor**.

## Structure
```text
anime-spark-analysis/
├── backend/
│   ├── app/
│   │   ├── services/ (analytics, Spark data access, prediction)
│   │   ├── config.py
│   │   └── routes.py
│   ├── requirements.txt
│   └── run.py
├── data/anime.csv
├── frontend/src/ (App.jsx, index.css, main.jsx)
├── models/anime_rating_model.pkl
├── output/anime_clean/ (Spark Parquet dataset)
└── spark/ (clean.py, analysis.py, model.py)
```

## Run on Windows

### 1. Backend (terminal one)
Use Python 3.11 if possible for better compatibility with PySpark and scientific Python packages.
```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python run.py
```
Check `http://127.0.0.1:5000/api/health`.

### 2. Frontend (terminal two)
```powershell
cd frontend
npm install
npm run dev
```
Open the Vite URL, normally `http://localhost:5173`.

### Configuration
The frontend defaults to `http://127.0.0.1:5000`. To change it, copy `frontend/.env.example` to `frontend/.env` and update `VITE_API_URL`.

## API
- `GET /api/health`
- `GET /api/stats`
- `GET /api/top-anime`
- `GET /api/type-analysis`
- `GET /api/genre-analysis`
- `GET /api/popular-anime`
- `GET /api/search?q=naruto`
- `POST /api/predict` with JSON `{"episodes":24,"members":50000,"type":"TV"}`

## Data and model
The API uses `output/anime_clean` when the Spark Parquet data exists, and falls back to `data/anime.csv` otherwise. The current model is expected at `models/anime_rating_model.pkl`. Rebuild cleaned data with `python spark/clean.py` or retrain with `python spark/model.py`, both from the project root. The large `rating.csv` events file was omitted because the current app doesn't use it; `anime.csv` is included.

## Troubleshooting
- If the page cannot connect, leave the backend terminal running and refresh.
- Use a supported Python and Java combination for PySpark.
- If model loading fails due to scikit-learn version differences, retrain the model in your environment.
