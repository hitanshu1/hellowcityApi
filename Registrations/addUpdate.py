import aioodbc
from ExceptionManager import mssqlExceptionManager
from aiohttp import web,web_request


# To add a patient to the database
async def addRegistrationFn(request, db_pool:aioodbc.Pool):
    return await _addUpdateFn(True, request, db_pool)


# To update a patient from the database
async def updateRegistrationFn(request, db_pool:aioodbc.Pool):
    return await _addUpdateFn(False, request, db_pool)


# To add/update an patient to the database
async def _addUpdateFn(toAdd, request:web_request.Request,db_pool:aioodbc.Pool):

    try:    
        data = await request.json()

        query = "INSERT INTO users(name, dateOfBirth, phone, email) VALUES (?, ?, ?, ?)"
        values = (data.get("name"), data.get("dateOfBirth"), data.get("phone"), data.get("email"))
        
        # pool = db_pool.pool 
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