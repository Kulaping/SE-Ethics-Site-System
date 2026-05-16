from flask import (Blueprint, request, jsonify, current_app, render_template)
from app.services.caching import Caching
from app.logger.logger import (log_info, log_warning)
from app.services.userpreference.preference import Prefencemanager
from app.utils.decorators import token_required
from urllib.parse import quote
import requests, time, json

news = Blueprint("news", __name__)
cacher = Caching()

#TODO: make a url_builder function to 
# avoid hardcoding the url build just to change a parameter.
'''
def url_builder(query, page_size, page, api_key)
'''     
   

@news.route("/news", methods=["GET"])
@token_required
def get_news(userID):
    try:
        page = int(request.args.get("page", 1))
        #page_size = 10
        #has_interacted = "q" in request.args
        query = request.args.get("section")
        log_info(f"Choosed query first hand: {query}")
        user = Prefencemanager(userID, query)
        pref_cat = user.get_highest_cat()
        #categories = ["News", "Business", "Entertainment", "General", "Health", "Science", "Sports", "Technology"]
        log_info(f"inside 'news' endpoint: {pref_cat}")
        log_info(f"Query received: {query}")
        log_info(f"user ID for news file: {userID}")
        
        if query and query != "world":
                  log_info("Changing Category....")
                  url = (
                            f"https://content.guardianapis.com/search"
                            f"?api-key={current_app.config['NEWS_API_KEY']}"
                            f"&show-fields=thumbnail,trailText,body&page={page}&section={query}"
                        )
                  cache_key = (query, page)
                   
                  if userID:
                      log_info(f"Updating user preference to: {query}")
                      user.update_preference()
        elif pref_cat:
             log_info('THIS FUCK FALLS')
             query = f'{pref_cat} AND "world"'
             log_info(f"enconded query: {query}")
             encoded_query = quote(query)
             url = (
                        f"https://content.guardianapis.com/search"
                        f"?api-key={current_app.config['NEWS_API_KEY']}"
                        f"&show-fields=thumbnail,trailText,body&page={page}&q={encoded_query}"
                   )
             cache_key = (query, page)
        
        else:
            log_info("Applying default category: news")
            url = (
                    f"https://content.guardianapis.com/search"
                    f"?api-key={current_app.config['NEWS_API_KEY']}"
                    f"&show-fields=thumbnail,trailText,body&page={page}&section={query}"
                  )
            cache_key = ("world", page)
            
        
        '''        
        else:
            log_warning("Failed processing the request.")
            return jsonify(
                {"status": False, 
                 "message": 
                     "The server's can't process your request. Try again later or enter a valid term."
                 })
        '''     
        
        cached_response = cacher.cache(cache_key)
        if cached_response:
            log_info(f"Cache hit: {cache_key}")
            log_info(f"caching res: {url}")
            return cached_response
        
        log_info(f"Cache miss: {cache_key}")
        log_info(f"outside: {url}")
        api_response = requests.get(url)
        api_response.raise_for_status()
        data = api_response.json()
        #pretty_json = json.dumps(data, indent=4)
        #log_info(pretty_json)

        cacher.setCache_func(cache_key, data)
     
        return jsonify(data)

    except requests.exceptions.RequestException as error:
        print("NewsAPI error:", error.response.text if error.response else str(error))
        return jsonify({"error": str(error)}), 500
