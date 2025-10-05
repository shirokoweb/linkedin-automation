import requests
from typing import Dict

class LinkedInAPI:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://api.linkedin.com/v2"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
    
    def get_user_profile(self) -> Dict:
        url = f"{self.base_url}/me"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def create_post(self, text: str, visibility: str = "PUBLIC") -> Dict:
        profile = self.get_user_profile()
        person_urn = f"urn:li:person:{profile['id']}"
        
        post_data = {
            "author": person_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": visibility
            }
        }
        
        url = f"{self.base_url}/ugcPosts"
        response = requests.post(url, headers=self.headers, json=post_data)
        response.raise_for_status()
        return response.json()
    
    def get_post_analytics(self, post_urn: str) -> Dict:
        url = f"{self.base_url}/socialActions/{post_urn}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
