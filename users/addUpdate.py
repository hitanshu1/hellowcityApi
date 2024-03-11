import aioodbc
from ExceptionManager import mssqlExceptionManager
from aiohttp import web,web_request
import hashlib

# To add a user to the database
async def addRegistrationFn(request, db_pool:aioodbc.Pool):
    return await _addUpdateFn(True, request, db_pool)


# To update a user from the database
async def updateRegistrationFn(request, db_pool:aioodbc.Pool):
    return await _addUpdateFn(False, request, db_pool)


# To add/update an user to the database
async def _addUpdateFn(toAdd, request:web_request.Request,db_pool:aioodbc.Pool):

    try:    
        data = await request.post()
        password_hash = hashlib.sha256(data.get("password").encode('utf-8')).hexdigest()

        # query = "INSERT INTO users(name, dateOfBirth, phone, email, password) VALUES (?, ?, ?, ?,?)"
        values = (data.get("name"), data.get("dateOfBirth"), data.get("phone"), data.get("email"),password_hash)
        
        if not toAdd:
            values += (data.get("id"),)
            query = "UPDATE users SET "
        else:
            query = "INSERT INTO users "

        if toAdd:
            
            query += "(name, dateOfBirth, phone, email,password,) "
            query += "VALUES (?, ?, ?, ?, ?) "
        else:
            query += "name=?, dateOfBirth=?, phone=?, email=?, password=? WHERE id=?"
         
        async with db_pool.acquire() as cnxn:
            async with cnxn.cursor() as cursor:
                await cursor.execute(query, values)
                await cnxn.commit() 
        
        success_response = {
            "message": f"{'Registration sccessful' if toAdd else 'updated successful'}!"
        }
        return web.json_response(success_response, status=200)

    except Exception as e:
    # Catch specific exceptions and provide a more meaningful error response
        error_message = {"error": str(e)}
        return web.json_response(error_message, status=500)