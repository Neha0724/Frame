from flask import Blueprint, jsonify, request
from app.services import analytics_service
from app.services.prediction_service import predict_rating
api = Blueprint('api', __name__)
@api.get('/health')
def health(): return jsonify({'status':'ok','service':'Frame Anime Data Studio API'})
@api.get('/stats')
def stats(): return jsonify(analytics_service.get_stats())
@api.get('/top-anime')
def top_anime(): return jsonify(analytics_service.top_anime())
@api.get('/type-analysis')
def type_analysis(): return jsonify(analytics_service.type_analysis())
@api.get('/genre-analysis')
def genre_analysis(): return jsonify(analytics_service.genre_analysis())
@api.get('/popular-anime')
def popular_anime(): return jsonify(analytics_service.popular_anime())
@api.get('/search')
def search():
    q=request.args.get('q','').strip()
    if not q: return jsonify([])
    if len(q)>120: return jsonify({'error':'Search query is too long.'}),400
    return jsonify(analytics_service.search_anime(q))
@api.post('/predict')
def predict():
    try: return jsonify({'predicted_rating':predict_rating(request.get_json(silent=True) or {})})
    except ValueError as e: return jsonify({'error':str(e)}),400
    except FileNotFoundError as e: return jsonify({'error':str(e)}),503
    except Exception: return jsonify({'error':'Prediction failed. Check model and dependency compatibility.'}),500
