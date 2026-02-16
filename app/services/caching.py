from flask import jsonify
import time

API_cache = {}
cache_duration = 60
#current_time = time.time()

class Caching:
      def cache(self, cache_keys):
            self.cache_keys = cache_keys
            
            try:
              if self.cache_keys in API_cache:
                now = time.time()
                if now - API_cache[self.cache_keys]["timestamp"] < cache_duration:
                   print("workingggggg")
                   return jsonify(API_cache[self.cache_keys]["data"])
               
            except Exception as e:
                print(e)
                return jsonify({"ok": False, "log": e})
               
            
      def setCache_func(self, cache_keys, data):
          now = time.time()
          
          API_cache[cache_keys] = {
              "data": data,
              "timestamp": now 
          }              