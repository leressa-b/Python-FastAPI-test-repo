from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import asyncio


class UserService:
    def __init__(self, database):
        self.db = database
    
    
    async def get_user(self, user_id: str):
        return await self.db.users.find_one({"_id": user_id})
    
    async def get_user_posts(self, user_id: str):
        return await self.db.posts.find({"user_id": user_id}).to_list(None)
    
    
    async def generate_activity_report(self, user_id: str, months: int = 12) -> Dict[str, Any]:

        user = await self.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        
        
        activities = await self.get_all_user_activities(user_id, months)
        
    
        report = {
            "user": user,
            "period": f"{months} months",
            "generated_at": datetime.now(),
            "summary": {},
            "monthly_breakdown": [],
            "top_content": {},
            "engagement": {},
            "trends": {}
        }
        
     
        report["summary"] = self.generate_summary(activities)
        report["monthly_breakdown"] = self.generate_monthly_breakdown(activities, months)
        report["top_content"] = self.generate_top_content(activities)
        report["engagement"] = self.generate_engagement_metrics(activities)
        report["trends"] = self.generate_trends(activities)
        
        return report
    
    async def get_all_user_activities(self, user_id: str, months: int) -> List[Dict[str, Any]]:
     
        start_date = datetime.now() - timedelta(days=30 * months)
        
      
        posts = await self.db.posts.find({
            "user_id": user_id,
            "created_at": {"$gte": start_date}
        }).to_list(None)
        
        comments = await self.db.comments.find({
            "user_id": user_id,
            "created_at": {"$gte": start_date}
        }).to_list(None)
        
        likes = await self.db.likes.find({
            "user_id": user_id,
            "created_at": {"$gte": start_date}
        }).to_list(None)
        
        shares = await self.db.shares.find({
            "user_id": user_id,
            "created_at": {"$gte": start_date}
        }).to_list(None)
        
       
        activities = []
        
        
        for post in posts:
            activities.append({
                "type": "post",
                "id": post["_id"],
                "title": post.get("title", ""),
                "content": post.get("content", ""),
                "created_at": post["created_at"],
                "likes": 0,
                "comments": 0,
                "shares": 0
            })
        
       
        for comment in comments:
            activities.append({
                "type": "comment",
                "id": comment["_id"],
                "content": comment.get("content", ""),
                "post_id": comment["post_id"],
                "created_at": comment["created_at"]
            })
        
      
        for like in likes:
            activities.append({
                "type": "like",
                "id": like["_id"],
                "target_id": like["target_id"],
                "target_type": like["target_type"],
                "created_at": like["created_at"]
            })
        
      
        for share in shares:
            activities.append({
                "type": "share",
                "id": share["_id"],
                "post_id": share["post_id"],
                "platform": share.get("platform", ""),
                "created_at": share["created_at"]
            })
        
        
        for activity in activities:
            if activity["type"] == "post":
               
                post_likes = await self.db.likes.find({
                    "target_id": activity["id"],
                    "target_type": "post"
                }).to_list(None)
                activity["likes"] = len(post_likes)
                
                
                post_comments = await self.db.comments.find({
                    "post_id": activity["id"]
                }).to_list(None)
                activity["comments"] = len(post_comments)
                
                
                post_shares = await self.db.shares.find({
                    "post_id": activity["id"]
                }).to_list(None)
                activity["shares"] = len(post_shares)
        
        return activities
    
    def generate_summary(self, activities: List[Dict[str, Any]]) -> Dict[str, Any]:
        
        summary = {
            "total_activities": len(activities),
            "posts": 0,
            "comments": 0,
            "likes": 0,
            "shares": 0,
            "avg_post_length": 0,
            "total_engagement": 0
        }
        
  
        for activity in activities:
            if activity["type"] == "post":
                summary["posts"] += 1
                summary["total_engagement"] += (
                    activity["likes"] + activity["comments"] + activity["shares"]
                )
            elif activity["type"] == "comment":
                summary["comments"] += 1
            elif activity["type"] == "like":
                summary["likes"] += 1
            elif activity["type"] == "share":
                summary["shares"] += 1
        
       
        posts = [a for a in activities if a["type"] == "post"]
        if posts:
            total_length = 0
            for post in posts:
                total_length += len(post.get("content", ""))
            summary["avg_post_length"] = round(total_length / len(posts))
        
        return summary
    
    def generate_monthly_breakdown(self, activities: List[Dict[str, Any]], months: int) -> List[Dict[str, Any]]:
      
        breakdown = []
        
    
        for i in range(months):
            date = datetime.now() - timedelta(days=30 * i)
            breakdown.append({
                "month": date.strftime("%B %Y"),
                "month_key": f"{date.year}-{date.month:02d}",
                "posts": 0,
                "comments": 0,
                "likes": 0,
                "shares": 0,
                "total_engagement": 0
            })
        
    
        for activity in activities:
            activity_date = activity["created_at"]
            activity_key = f"{activity_date.year}-{activity_date.month:02d}"
            
      
            for month in breakdown:
                if month["month_key"] == activity_key:
                    if activity["type"] == "post":
                        month["posts"] += 1
                        month["total_engagement"] += (
                            activity["likes"] + activity["comments"] + activity["shares"]
                        )
                    elif activity["type"] == "comment":
                        month["comments"] += 1
                    elif activity["type"] == "like":
                        month["likes"] += 1
                    elif activity["type"] == "share":
                        month["shares"] += 1
                    break
        
        return list(reversed(breakdown))
    
    def generate_top_content(self, activities: List[Dict[str, Any]]) -> Dict[str, Any]:
        
        posts = [a for a in activities if a["type"] == "post"]
        
      
        top_by_likes = sorted(posts, key=lambda x: x["likes"], reverse=True)[:5]
        top_by_comments = sorted(posts, key=lambda x: x["comments"], reverse=True)[:5]
        top_by_shares = sorted(posts, key=lambda x: x["shares"], reverse=True)[:5]
        
     
        posts_with_scores = []
        for post in posts:
            engagement_score = (post["likes"] * 1) + (post["comments"] * 2) + (post["shares"] * 3)
            posts_with_scores.append({**post, "engagement_score": engagement_score})
        
        top_by_engagement = sorted(posts_with_scores, key=lambda x: x["engagement_score"], reverse=True)[:5]
        
        return {
            "top_by_likes": top_by_likes,
            "top_by_comments": top_by_comments,
            "top_by_shares": top_by_shares,
            "top_by_engagement": top_by_engagement
        }
    
    def generate_engagement_metrics(self, activities: List[Dict[str, Any]]) -> Dict[str, Any]:
       
        posts = [a for a in activities if a["type"] == "post"]
        comments = [a for a in activities if a["type"] == "comment"]
        likes = [a for a in activities if a["type"] == "like"]
        shares = [a for a in activities if a["type"] == "share"]
        
       
        total_post_likes = 0
        total_post_comments = 0
        total_post_shares = 0
        
        for post in posts:
            total_post_likes += post["likes"]
            total_post_comments += post["comments"]
            total_post_shares += post["shares"]
        
       
        avg_likes_per_post = total_post_likes / len(posts) if posts else 0
        avg_comments_per_post = total_post_comments / len(posts) if posts else 0
        avg_shares_per_post = total_post_shares / len(posts) if posts else 0
        
      
        day_of_week_stats = {}
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        for day in days_of_week:
            day_of_week_stats[day] = {"posts": 0, "total_engagement": 0}
        
        for activity in activities:
            if activity["type"] == "post":
                day_of_week = activity["created_at"].strftime("%A")
                day_of_week_stats[day_of_week]["posts"] += 1
                day_of_week_stats[day_of_week]["total_engagement"] += (
                    activity["likes"] + activity["comments"] + activity["shares"]
                )
        
      
        best_day = ""
        best_engagement = 0
        for day in days_of_week:
            avg_engagement = (
                day_of_week_stats[day]["total_engagement"] / day_of_week_stats[day]["posts"]
                if day_of_week_stats[day]["posts"] > 0 else 0
            )
            
            if avg_engagement > best_engagement:
                best_engagement = avg_engagement
                best_day = day
        
        return {
            "avg_likes_per_post": round(avg_likes_per_post, 2),
            "avg_comments_per_post": round(avg_comments_per_post, 2),
            "avg_shares_per_post": round(avg_shares_per_post, 2),
            "total_engagement": total_post_likes + total_post_comments + total_post_shares,
            "engagement_rate": round(
                (total_post_likes + total_post_comments + total_post_shares) / len(posts), 2
            ) if posts else 0,
            "best_day_to_post": best_day,
            "day_of_week_stats": day_of_week_stats
        }
    
    def generate_trends(self, activities: List[Dict[str, Any]]) -> Dict[str, Any]:
       
        posts = [a for a in activities if a["type"] == "post"]
        
    
        trends = {
            "post_frequency": "stable",
            "engagement_trend": "stable",
            "content_length": "stable",
            "weekly_pattern": []
        }
        
        
        weeks = {}
        for post in posts:
            week_key = self.get_week_key(post["created_at"])
            if week_key not in weeks:
                weeks[week_key] = {"posts": 0, "total_engagement": 0}
            weeks[week_key]["posts"] += 1
            weeks[week_key]["total_engagement"] += (
                post["likes"] + post["comments"] + post["shares"]
            )
        
        
        weekly_data = []
        for week, data in weeks.items():
            avg_engagement = data["total_engagement"] / data["posts"] if data["posts"] > 0 else 0
            weekly_data.append({
                "week": week,
                "posts": data["posts"],
                "avg_engagement": avg_engagement
            })
        
        weekly_data.sort(key=lambda x: x["week"])
        trends["weekly_pattern"] = weekly_data
        
        
        if len(weekly_data) >= 4:
            recent = weekly_data[-4:]
            older = weekly_data[:4]
            
            recent_avg_posts = sum(week["posts"] for week in recent) / len(recent)
            older_avg_posts = sum(week["posts"] for week in older) / len(older)
            
            if recent_avg_posts > older_avg_posts * 1.1:
                trends["post_frequency"] = "increasing"
            elif recent_avg_posts < older_avg_posts * 0.9:
                trends["post_frequency"] = "decreasing"
        
        return trends
    
    def get_week_key(self, date: datetime) -> str:
        
        year = date.year
        week = date.isocalendar()[1]
        return f"{year}-W{week:02d}"



async def main():

   
    class MockDatabase:
        def __init__(self):
            self.users = self
            self.posts = self
            self.comments = self
            self.likes = self
            self.shares = self
        
        async def find_one(self, query):
            return {"_id": "user123", "name": "Test User"}
        
        async def find(self, query):
            return self
        
        async def to_list(self, limit):
            return []
    

    db = MockDatabase()
    service = UserService(db)
    
    try:
        report = await service.generate_activity_report("user123", 6)
        print("Report generated successfully!")
        print(f"Report keys: {list(report.keys())}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

