from functools import lru_cache
import joblib
import pandas as pd
from app.config import MODEL_PATH

@lru_cache(maxsize=1)
def get_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f'Trained model not found: {MODEL_PATH}. Run python spark/model.py from project root.')
    return joblib.load(MODEL_PATH)

def predict_rating(payload):
    episodes, members, anime_type = payload.get('episodes'), payload.get('members'), payload.get('type')
    if episodes is None or members is None or not anime_type:
        raise ValueError('episodes, members and type are required.')
    try: episodes, members = float(episodes), float(members)
    except (TypeError, ValueError): raise ValueError('Episodes and members must be numeric.')
    if episodes <= 0 or members <= 0: raise ValueError('Episodes and members must be greater than zero.')
    frame = pd.DataFrame([{'episodes_num':episodes,'members_num':members,'type':str(anime_type).strip()}])
    value = float(get_model().predict(frame)[0])
    return round(max(0.0, min(10.0, value)), 2)
