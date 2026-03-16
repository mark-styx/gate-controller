from gate_control import REVERE
from gate_control.__classes__.Events import event
from gate_control.config import API_KEY, ACTIONS

from flask import Flask,request,jsonify
from datetime import datetime as dt
from time import sleep
from functools import wraps

ts = lambda:dt.now().timestamp()

app = Flask(__name__)

def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for API key in header or query parameter
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        if not api_key:
            return jsonify({'error': 'Missing API key'}), 401
        
        if api_key != API_KEY:
            return jsonify({'error': 'Invalid API key'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def validate_json_request(f):
    """Decorator to validate JSON request body"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'POST' and not request.is_json:
            # Allow empty body for POST, but validate if present
            pass
        return f(*args, **kwargs)
    return decorated_function

@app.route('/health', methods=['get'])
def health_check():
    """Health check endpoint - no auth required"""
    try:
        # Check Redis connection
        REVERE.ping()
        redis_status = 'ok'
    except Exception as e:
        redis_status = f'error: {str(e)}'
    
    return jsonify({
        'status': 'healthy' if redis_status == 'ok' else 'degraded',
        'redis': redis_status,
        'timestamp': ts()
    })

@app.route('/gate/activate', methods=['post'])
@require_api_key
@validate_json_request
def gate_activate():
   try:
      # Validate mock parameter if present
      if request.json:
         mock = request.json.get('mock')
         if mock is not None and not isinstance(mock, bool):
            return jsonify({'error': 'Invalid mock parameter, must be boolean'}), 400
         
         if mock:
            msg = 'Mock Activate Request'
            print(msg)
            return jsonify({'message': msg})
      
      event('activate',source='api')
      sleep(1.5)
      state = REVERE.get("state")
      return jsonify({'state': state, 'message': 'Gate activation initiated'})
   except ValueError as e:
      return jsonify({'error': str(e)}), 400
   except Exception as e:
      return jsonify({'error': f'Failed to activate gate: {str(e)}'}), 500

@app.route('/gate/status', methods=['get'])
@require_api_key
def gate_status():
   try:
      state = REVERE.get("state")
      ebrake = REVERE.get("ebrake")
      return jsonify({
         'state': state,
         'ebrake': ebrake
      })
   except Exception as e:
      return jsonify({'error': f'Failed to get status: {str(e)}'}), 500

@app.route('/gate/ebrake', methods=['post','get'])
@require_api_key
def gate_ebrake():
   try:
      ebrake = REVERE.get('ebrake')
      if request.method.lower() == 'get':
         return jsonify({'ebrake': ebrake})
      
      # POST - toggle ebrake
      if request.json:
         mock = request.json.get('mock')
         if mock is not None and not isinstance(mock, bool):
            return jsonify({'error': 'Invalid mock parameter, must be boolean'}), 400
         
         if mock:
            msg = 'Mock ebrake Request'
            print(msg)
            return jsonify({'message': msg})
      
      event('ebrake',source='api')
      return jsonify({'message': 'Toggling ebrake', 'previous_state': ebrake})
   except ValueError as e:
      return jsonify({'error': str(e)}), 400
   except Exception as e:
      return jsonify({'error': f'Failed to toggle ebrake: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
   return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
   return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(port=8081)
