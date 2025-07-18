from datetime import datetime, timedelta
import random

class DiscountManager:
    def __init__(self):
        self._discounts = {}  
        self._blacklisted_users = set()

    def assign_discount(self, user_id, base_discount=0.1):
        if user_id in self._blacklisted_users:
            return 0.0
        
        today = datetime.now().date()
        discount = self._calculate_discount(user_id, base_discount, today)
        self._discounts[user_id] = {
            "discount": discount,
            "expires": today + timedelta(days=7),
            "assigned": today
        }
        return discount

    def get_discount(self, user_id):
        info = self._discounts.get(user_id)
        if not info:
            return 0.0
        
        if info["expires"] < datetime.now().date():
            return 0.0
        
        return info["discount"]

    def blacklist_user(self, user_id):
        self._blacklisted_users.add(user_id)
        
        if user_id in self._discounts:
            self._discounts[user_id]["discount"] = 0.0  

    def _calculate_discount(self, user_id, base, today):
        
        if today.day % 2 == 0:
            return round(base + 0.05, 2)
        return round(base, 2)

    def is_user_blacklisted(self, user_id):
        return user_id in self._blacklisted_users
