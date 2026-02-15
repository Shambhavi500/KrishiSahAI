import os
import httpx
import asyncio

class NewsService:
    def __init__(self):
        self.api_key = os.getenv("GNEWS_API_KEY")
        self.base_url = "https://gnews.io/api/v4"
        if not self.api_key:
             print("Warning: GNEWS_API_KEY not found in environment variables.")

    async def get_personalized_news(self, crops: list, location: str = "India"):
        """
        Fetches personalized news based on crops and location.
        Prioritizes local news when specific location is provided.
        """
        if not self.api_key:
             return {"error": "News API key not configured"}
             
        query = self._generate_news_query(crops, location, personalized=True)
        
        url = f"{self.base_url}/search"
        params = {
            "q": query,
            "lang": "en", # Default to English for now, API supports others
            "country": "in",
            "max": 10,  # Increased to get more local results
            "apikey": self.api_key
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                return self.preprocess_news(data)
            except httpx.RequestError as e:
                print(f"News API Request Error: {e}")
                return {"error": f"Failed to connect to News API: {str(e)}"}
            except httpx.HTTPStatusError as e:
                print(f"News API Status Error: {e}")
                return {"error": f"News API returned error: {e.response.status_code}"}
            except Exception as e:
                 print(f"News Service Error: {e}")
                 return {"error": f"An unexpected error occurred: {str(e)}"}

    async def get_general_news(self):
        """
        Fetches general agriculture and farming news for India.
        """
        if not self.api_key:
             return {"error": "News API key not configured"}
             
        query = self._generate_news_query([], "India", personalized=False)
        
        url = f"{self.base_url}/search"
        params = {
            "q": query,
            "lang": "en",
            "country": "in",
            "max": 10,
            "apikey": self.api_key
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                data = response.json()
                return self.preprocess_news(data)
            except httpx.RequestError as e:
                print(f"News API Request Error: {e}")
                return {"error": f"Failed to connect to News API: {str(e)}"}
            except httpx.HTTPStatusError as e:
                print(f"News API Status Error: {e}")
                return {"error": f"News API returned error: {e.response.status_code}"}
            except Exception as e:
                 print(f"News Service Error: {e}")
                 return {"error": f"An unexpected error occurred: {str(e)}"}

    def _generate_news_query(self, crops, location, personalized=True):
        """
        Generates a search query for GNews.
        For personalized: Prioritizes crop + location specific news
        For general: Broad agriculture news
        """
        if personalized and crops:
            # Personalized mode: Focus on specific crops
            crop_terms = " OR ".join([f'"{c}"' for c in crops])
            crop_query = f"({crop_terms})"
            
            # Add farming context
            query = f"{crop_query} AND (farming OR agriculture OR cultivation OR harvest)"
            
            # Add location for local news priority
            if location and location.lower() not in ["unknown", "india"]:
                # Prioritize location-specific news
                query += f' AND "{location}"'
        else:
            # General mode: Broad agriculture news
            query = "(agriculture OR farming OR crops OR irrigation OR fertilizer OR seeds)"
            query += " AND (news OR update OR technology OR innovation OR government OR scheme)"
            
        return query

    def preprocess_news(self, raw_data):
        """
        Keeps only: headline, source, short summary, url
        """
        if not raw_data or "articles" not in raw_data:
            return []
            
        articles = raw_data.get("articles", [])
        processed = []
        
        for article in articles:
            summary = article.get("description", "")
            if summary and len(summary) > 200:
                summary = summary[:197] + "..."
                
            processed.append({
                "headline": article.get("title"),
                "source": article.get("source", {}).get("name"),
                "summary": summary,
                "url": article.get("url"),
                "published_at": article.get("publishedAt"),
                "image": article.get("image"), # Helpful for UI
                "content": article.get("content") # Full/Truncated content
            })
            
        return processed

# Usage example
if __name__ == "__main__":
    async def main():
        service = NewsService()
        news = await service.get_personalized_news(["wheat", "rice"], "Punjab")
        print(news)
    # asyncio.run(main())
