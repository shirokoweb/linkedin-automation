from flask import Blueprint, jsonify
from app.models import Post, Analytics, get_db
from datetime import datetime
import os

monitor_bp = Blueprint('monitor', __name__)

@monitor_bp.route('/dashboard')
def dashboard():
    db = get_db()
    
    total_posts = db.query(Post).count()
    published = db.query(Post).filter(Post.status == 'published').count()
    scheduled = db.query(Post).filter(Post.status == 'draft').count()
    
    stats = {
        'total_posts': total_posts,
        'published': published,
        'scheduled': scheduled
    }
    
    html = f"""
    <html>
    <head><title>LinkedIn Automation Dashboard</title></head>
    <body style="font-family: Arial; padding: 40px; background: #f5f5f5;">
        <h1>📊 LinkedIn Automation Dashboard</h1>
        <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h2>Statistics</h2>
            <p><strong>Total Posts:</strong> {stats['total_posts']}</p>
            <p><strong>Published:</strong> {stats['published']}</p>
            <p><strong>Scheduled:</strong> {stats['scheduled']}</p>
        </div>
        <div style="background: white; padding: 20px; border-radius: 8px;">
            <h2>Quick Actions</h2>
            <a href="/oauth/start" style="display: inline-block; padding: 10px 20px; background: #0a66c2; color: white; text-decoration: none; border-radius: 4px; margin: 5px;">Authenticate LinkedIn</a>
            <a href="/oauth/status" style="display: inline-block; padding: 10px 20px; background: #6c757d; color: white; text-decoration: none; border-radius: 4px; margin: 5px;">Check Auth Status</a>
            <a href="/api/posts" style="display: inline-block; padding: 10px 20px; background: #28a745; color: white; text-decoration: none; border-radius: 4px; margin: 5px;">View Posts API</a>
        </div>
    </body>
    </html>
    """
    return html

@monitor_bp.route('/health/detailed')
def health_detailed():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })
