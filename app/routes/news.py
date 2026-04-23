from flask import Blueprint, request, jsonify, current_app
from app.services.caching import Caching
from app.logger.logger import log_info, log_warning
from app.services.userpreference.preference import Prefencemanager
from app.utils.decorators import token_required
import requests, time

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
        page_size = 10
        #has_interacted = "q" in request.args
        query = request.args.get("q")
        log_info(f"Choosed query first hand: {query}")
        user = Prefencemanager(userID, query)
        pref_cat = user.get_highest_cat()
        log_info(f"pref_cat: {pref_cat}")

        #is_global_request = (query == "")
       # pref_cat = None

        log_info(f"Query received: {query}")
        log_info(f"user ID for news file: {userID}")
        
        '''
        if query: 
                url = (
                    f"https://newsapi.org/v2/everything"
                    f"?q={query}&pageSize={page_size}&page={page}"
                    f"&apiKey={current_app.config['NEWS_API_KEY']}"
                )
                cache_key = (query, page)
              
                if userID:
                         log_info(f"user: {user}")
                         user.update_preference() 
                else:
                    log_warning("No token")
                   
        elif pref_cat: 
             log_info(f"Testing if this shit does not cause race conditions for: {pref_cat}")
             url = (
                f"https://newsapi.org/v2/everything"
                f"?q={pref_cat}&pageSize={page_size}&page={page}"
                f"&apiKey={current_app.config['NEWS_API_KEY']}"
             )
             log_info(f"inside conditionals: {url}")
             cache_key = (pref_cat, page)
        
        else:
            url = (
                    f"https://newsapi.org/v2/everything"
                    f"?q=news&pageSize={page_size}&page={page}"
                    f"&apiKey={current_app.config['NEWS_API_KEY']}"
            )
            cache_key = (None, page)
        '''
        
        #TODO: FIXING THIS PIECE OF CRAP I WROTE.
        
        if query and query != "news":
               #search_term = query if query else "news"
                   log_info("Changing Category....")
                   url = (
                         f"https://newsapi.org/v2/everything"
                         f"?q={query}&pageSize={page_size}&page={page}"
                         f"&apiKey={current_app.config['NEWS_API_KEY']}"
                   )
                   cache_key = (query if query else "news", page)
                   
                   if userID:
                      log_info(f"Updating user preference to: {query}")
                      user.update_preference()
             
        elif pref_cat:
           
             log_info(f"First load - applying preference: {pref_cat}")
             url = (
                   f"https://newsapi.org/v2/everything"
                   f"?q={pref_cat}&pageSize={page_size}&page={page}"
                   f"&apiKey={current_app.config['NEWS_API_KEY']}"
             )
             cache_key = (pref_cat, page)
        
        else: 
             log_info(f"Applying default category: news")
             url = (
                   f"https://newsapi.org/v2/everything"
                   f"?q=news&pageSize={page_size}&page={page}"
                   f"&apiKey={current_app.config['NEWS_API_KEY']}"
             )
             cache_key = ("news", page)
        
        
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

        cacher.setCache_func(cache_key, data)
        log_info(f"if it has raise condition: {pref_cat}")
     
        return jsonify(data)

    except requests.exceptions.RequestException as error:
        print("NewsAPI error:", error.response.text if error.response else str(error))
        return jsonify({"error": str(error)}), 500


'''
        else:
            log_warning("Failed processing the request.")
            return jsonify(
                {"status": False, 
                 "message": 
                     "The server's can't process your request. Try again later or enter a valid term."
                 })
 '''