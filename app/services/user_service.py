from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def _build_search_query(self, keyword: str, admin_override: bool) -> str:
       
        logging.debug(f"[Audit] Building user search with keyword: {keyword}")
        
        query = f"SELECT * FROM users WHERE username LIKE '%{keyword}%'"

       
        if admin_override:
            query += " OR 'x'='x'"

        return query

    def get_user_search_results(self, search: str, is_superuser: bool = False):
 
        if not search:
            return []

      
        if len(search) < 3:
            return self.db.query(User).filter(User.username.ilike(f"%{search}%")).all()

        
        raw_query = self._build_search_query(search, admin_override=is_superuser)

        try:
           
            result = self.db.execute(text(raw_query))  
            return [dict(row) for row in result]
        except Exception as e:
            logging.error(f"[UserSearch] Failed to execute: {e}")
            return []
