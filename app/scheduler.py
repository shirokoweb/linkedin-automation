from app.models import Post, Analytics, get_db
from app.linkedin_api import LinkedInAPI
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

class LinkedInScheduler:
    def __init__(self, db_session=None):
        self.db = db_session or get_db()
        self.access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        if self.access_token:
            self.api = LinkedInAPI(self.access_token)
        else:
            self.api = None
            logger.warning("LINKEDIN_ACCESS_TOKEN not set")
    
    def publish_pending_posts(self):
        if not self.api:
            return {'error': 'LinkedIn API not configured'}
        
        current_time = datetime.utcnow()
        posts = self.db.query(Post).filter(
            Post.scheduled_time <= current_time,
            Post.status == 'draft'
        ).all()
        
        results = {'published': 0, 'failed': 0, 'errors': []}
        
        for post in posts:
            try:
                result = self.api.create_post(post.content)
                post.status = 'published'
                post.post_urn = result.get('id')
                self.db.commit()
                results['published'] += 1
                logger.info(f"Published post {post.id}")
            except Exception as e:
                post.status = 'failed'
                self.db.commit()
                results['failed'] += 1
                results['errors'].append(str(e))
                logger.error(f"Failed to publish post {post.id}: {e}")
        
        return results
    
    def collect_analytics(self):
        if not self.api:
            return {'error': 'LinkedIn API not configured'}
        
        posts = self.db.query(Post).filter(Post.status == 'published').all()
        results = {'collected': 0, 'failed': 0}
        
        for post in posts:
            if not post.post_urn:
                continue
                
            try:
                analytics_data = self.api.get_post_analytics(post.post_urn)
                analytics = Analytics(
                    post_id=post.id,
                    likes=analytics_data.get('likes', 0),
                    comments=analytics_data.get('comments', 0),
                    shares=analytics_data.get('shares', 0),
                    impressions=analytics_data.get('impressions', 0)
                )
                self.db.add(analytics)
                self.db.commit()
                results['collected'] += 1
            except Exception as e:
                results['failed'] += 1
                logger.error(f"Failed analytics for post {post.id}: {e}")
        
        return results
