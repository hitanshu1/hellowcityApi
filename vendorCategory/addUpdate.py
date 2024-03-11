import aioodbc
from ExceptionManager import mssqlExceptionManager
from aiohttp import web,web_request
import hashlib

from access_token import AccessToken

# To add a vendor to the database
@AccessToken.token_required
async def addVendorCategory(request, db_pool:aioodbc.Pool):
    return await _addUpdateFn(True, request, db_pool)


# To update a vendor from the database
@AccessToken.token_required
async def updateVendorCategory(request, db_pool:aioodbc.Pool):
    return await _addUpdateFn(False, request, db_pool)


# To add/update an vendor to the database
async def _addUpdateFn(toAdd, request:web_request.Request,db_pool:aioodbc.Pool):

    try:    
        data = await request.post()
        values = (data.get("name"),data.get("menuID"), data.get('status'))

        if not toAdd:
            values += (data.get("id"),)
            query = "UPDATE vendorCategory SET "
        else:
            query = "INSERT INTO vendorCategory "

        if toAdd:
            query += "(name,menuID,status) "
            query += "VALUES (?, ?,?) "
        else:
            query += "name=?,menuID=?,status=? WHERE id=?"
        
        async with db_pool.acquire() as cnxn:
            async with cnxn.cursor() as cursor:
                await cursor.execute(query, values)
                await cnxn.commit() 
        
        success_response = {
            "message": f"{'added sccessfully' if toAdd else 'updated successfully'}!"
        }
        return web.json_response(success_response, status=200)

    except Exception as e:
    # Catch specific exceptions and provide a more meaningful error response
        error_message = {"error": str(e)}
        return web.json_response(error_message, status=500)