from flask import (Blueprint, request, jsonify, current_app)
from app.services.caching import Caching
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

news =  Blueprint("news", __name__)
#news_cache = {}
#cache_duration = 60
cacher = Caching()

@news.route("/news", methods=["GET"])
def get_news():
   
    page = int(request.args.get("page", 1))
    QUERY = request.args.get("q")
    logger.info(QUERY)
    pageSize = 10
   # current_time = time.time()
    
    URL = f"https://newsapi.org/v2/everything?q={QUERY}&pageSize={pageSize}&page={page}&apiKey={current_app.config['NEWS_API_KEY']}"
    
    cache_key = (QUERY, page)
    cached_response = cacher.cache(cache_key)
    
    if cached_response:
       return cached_response
    
    try:
      
       data = requests.get(URL)
       if data.status_code == 429:
            return jsonify({"message": "Rate limit exceeded"}), 429
       
       data.raise_for_status()
       news = data.json()
       #print(news)
       
      # titles = [article["title"] for article in news["articles"]]
       #print(" , ".join(titles))
       
       cacher.setCache_func(cache_key, news)
       
       return jsonify(news)  
    
    except requests.exceptions.RequestException as error:
       #DEBUGGGGGGGG:
       print("NewsAPI error:", error.response.text if error.response else str(error))
       return jsonify({"error": str(error)}), 500