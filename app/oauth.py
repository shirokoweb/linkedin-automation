from flask import Blueprint, request, redirect, jsonify, session
import requests
import secrets
import os
import json
from datetime import datetime

oauth_bp = Blueprint('oauth', __name__)

AUTHORIZATION_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
SCOPES = "r_liteprofile r_emailaddress w_member_social"

def get_oauth_config():
    return {
        'client_id': os.getenv('LINKEDIN_CLIENT_ID'),
        'client_secret': os.getenv('LINKEDIN_CLIENT_SECRET'),
        'redirect_uri': os.getenv('LINKEDIN_REDIRECT_URI')
    }

@oauth_bp.route('/oauth/start')
def oauth_start():
    config = get_oauth_config()
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state
    
    params = {
        'response_type': 'code',
        'client_id': config['client_id'],
        'redirect_uri': config['redirect_uri'],
        'state': state,
        'scope': SCOPES
    }
    
    auth_url = f"{AUTHORIZATION_URL}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    return redirect(auth_url)

@oauth_bp.route('/oauth/callback')
def oauth_callback():
    state = request.args.get('state')
    if state != session.get('oauth_state'):
        return jsonify({'error': 'Invalid state'}), 400
    
    code = request.args.get('code')
    if not code:
        return jsonify({'error': 'No authorization code'}), 400
    
    config = get_oauth_config()
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': config['redirect_uri'],
        'client_id': config['client_id'],
        'client_secret': config['client_secret']
    }
    
    try:
        response = requests.post(TOKEN_URL, data=token_data)
        response.raise_for_status()
        token_response = response.json()
        
        access_token = token_response['access_token']
        
        token_file_path = '/var/www/webroot/ROOT/config/linkedin_token.json'
        os.makedirs(os.path.dirname(token_file_path), exist_ok=True)
        
        with open(token_file_path, 'w') as f:
            json.dump({
                'access_token': access_token,
                'obtained_at': str(datetime.utcnow())
            }, f)
        
        os.environ['LINKEDIN_ACCESS_TOKEN'] = access_token
        
        return f"<h1>✓ Authentication Successful!</h1><p>Token saved. You can close this window.</p><p><a href='/dashboard'>Go to Dashboard</a></p>"
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@oauth_bp.route('/oauth/status')
def oauth_status():
    token = os.getenv('LINKEDIN_ACCESS_TOKEN')
    if token:
        return jsonify({'authenticated': True, 'token_preview': token[:20] + '...'})
    return jsonify({'authenticated': False})
