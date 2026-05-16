from app.models.models import db, userPreference
from app.logger.logger import log_info, log_warning
import json

class Prefencemanager:
      
      def __init__(self, user_id, category=None):
         self.user_id = user_id
         self.category = category
      
      def update_preference(self):
        
          if self.category:
                  log_info(True)
                  pref = userPreference.query.filter_by(user_id=self.user_id, categories=self.category).first()

                  if pref:
                      pref.weight += 1
                      log_info("hit, updating preference")

                  else:
                      pref = userPreference(user_id=self.user_id, categories=self.category, weight=1)
                      db.session.add(pref)
                      log_info("creating new row")
                      
                  db.session.commit()      
        
      def get_highest_cat(self):
          log_info("The function's running")
          top_pref = (userPreference.query.filter_by(user_id=self.user_id).order_by(userPreference.weight.desc()).first())     
        
          if top_pref is None: 
             log_warning("No Query/Cat")
             return None
            
          log_info(f"TOP CATEGORY: {top_pref.categories}: {top_pref.weight}")
          max_categories = top_pref.categories             
          log_info(f"user categories: {top_pref.categories} {top_pref.weight}")
                #log_warning(f"working status. clicked query: {self.category}")
          log_info(f"computation: {top_pref.categories} {top_pref.weight}")
          print(f"cat: {max_categories}")
          
          return max_categories

          
'''         
         debug_list = [{"id": r.id, "user": r.user_id, "cat": r.categories, "weight": r.weight} 
                       for r in all_records]
    
                    print(len(all_records))
                     print(json.dumps(debug_list, indent=4))
'''
             
            

'''
class returnMaxcatValue(prefenceManager):
      def __init__(self):
          super().__init__(user_id, category)     
'''