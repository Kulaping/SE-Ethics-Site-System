from flask import (Blueprint, request, jsonify, current_app)
from app.services.caching import Caching
import requests, time, logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

weather_bp = Blueprint("weather", __name__)

'''
weather_cache = {}
cache_duration = 60
Time = time.time() 
'''
cacher = Caching()

@weather_bp.route("/weather", methods=["POST"])
def get_weather(): 
    data = request.get_json()
    lat = data.get('lat')
    lon = data.get('lon')
    cache_key = (str(lat), str(lon))
    start = time.time()
    
    cached_weather = cacher.cache(cache_key)
   
    if cached_weather:
       elapsed = time.time() - start
       print(f"Cache hit for weather. Elapsed time:{elapsed:.6f}s")
       return cached_weather
    else:
       logger.warning("Missed Cache")

    
    if not lat or not lon:
       return jsonify({'error': 'No/Missing Coordinates'}), 400
    
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={current_app.config['WEATHER_API_KEY']}&units=metric"
    
    try: 
       
       start = time.time() - start
       response = requests.get(url)
       response.raise_for_status()
       weather = response.json()
       elapsed = time.time() - start
       logger.info(f"Cache hit for weather. Elapsed time:{elapsed:.6f}s")
       
       cacher.setCache_func(cache_key, weather)     
       
       return jsonify(weather)
    
    except requests.exceptions.RequestException as error:
       return jsonify({"error": str(error)}), 500