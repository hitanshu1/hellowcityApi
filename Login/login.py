
import hashlib
import aioodbc
from ExceptionManager import mssqlExceptionManager
from aiohttp import web, web_request


from access_token import AccessToken



# To login a user for the given email & password
async def loginFn(request:web_request.Request, db_pool:aioodbc.Pool):
    try:
        data = await request.post()
        email = data.get("email")
        password = data.get("password")
        password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        query = f"SELECT * FROM users WHERE email = '{email}' AND password = '{password_hash}'"
        
        async with db_pool.acquire() as cnxn:
            async with cnxn.cursor() as cursor:
                await cursor.execute(query)
                row = await cursor.fetchone()
            
                # print(create_access_token(row[0]))
                if row:
                    user_details = {
                        'id': row[0],
                        'name': row[1],
                        'dateOfBirth': row[2],
                        'phone': row[3],
                        'email': row[4],
                        'token': AccessToken.generate_access_token(row[0])  # Generate JWT token
                    }
                    print(user_details)
                    # result_json = json.dumps(user_details, indent=4, default=str)
                    return web.json_response(user_details, content_type="application/json")
                else:
                    return web.json_response({'error': 'Invalid email or password'}, status=401)
    except Exception as e:
        # Handle exceptions
        return await mssqlExceptionManager(e)


    
