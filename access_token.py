import jwt
from functools import wraps
from aiohttp import web ,web_request
from datetime import datetime, timedelta

SECRET_KEY = '8055' 
class AccessToken:
   def token_required(f):
    @wraps(f)
    async def decorated(request, *args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return web.json_response({'message': 'Token is missing'}, status=401)

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return web.json_response({'message': 'Token has expired'}, status=401)
        except jwt.InvalidTokenError:
            return web.json_response({'message': 'Token is invalid'}, status=401)

        return await f(request, *args, **kwargs)

    return decorated
   
   def generate_access_token(user_id,):
    # Calculate expiry time
    expiry_time = datetime.utcnow() + timedelta(days=365)

    # Create payload for the token
    payload = {
        'user_id': user_id,
        'exp': expiry_time,
    }

    # Generate the token
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return token