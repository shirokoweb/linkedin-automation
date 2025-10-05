from flask import Blueprint, jsonify, request
from app.models import Post, Analytics, get_db
from datetime import datetime

api_bp = Blueprint('api', __name__)

@api_bp.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

@api_bp.route('/posts', methods=['GET'])
def get_posts():
    db = get_db()
    posts = db.query(Post).order_by(Post.created_at.desc()).limit(50).all()
    return jsonify([{
        'id': p.id,
        'content': p.content[:100] + '...' if len(p.content) > 100 else p.content,
        'status': p.status,
        'scheduled_time': p.scheduled_time.isoformat() if p.scheduled_time else None
    } for p in posts])

@api_bp.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    db = get_db()
    
    post = Post(
        content=data['content'],
        image_path=data.get('image_path'),
        scheduled_time=datetime.fromisoformat(data['scheduled_time']) if data.get('scheduled_time') else None
    )
    db.add(post)
    db.commit()
    
    post_id = post.id
    db.close()
    
    return jsonify({'id': post_id, 'status': 'created'}), 201

@api_bp.route('/analytics', methods=['GET'])
def get_analytics():
    db = get_db()
    analytics = db.query(Analytics).order_by(Analytics.checked_at.desc()).limit(100).all()
    db.close()
    
    return jsonify([{
        'post_id': a.post_id,
        'likes': a.likes,
        'comments': a.comments,
        'shares': a.shares,
        'impressions': a.impressions,
        'checked_at': a.checked_at.isoformat()
    } for a in analytics])
