# Backend

Flask REST endpoints, Apache Spark analytics, and scikit-learn prediction.

```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.bat
pip install -r requirements.txt
python run.py
```
API health check: `http://127.0.0.1:5000/api/health`. Dataset/model paths are resolved from the project root, not the working directory.
