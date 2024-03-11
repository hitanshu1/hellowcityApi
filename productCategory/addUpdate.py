import aioodbc
from ExceptionManager import mssqlExceptionManager
from aiohttp import web,web_request
import hashlib

from access_token import AccessToken

# To add a vendor to the database
@AccessToken.token_required
async def addProductCategory(request, db_pool:aioodbc.Pool):
    return await _addUpdateFn(True, request, db_pool)


# To update a ProductCategory from the database
@AccessToken.token_required
async def updateProductCategory(request, db_pool:aioodbc.Pool):
    return await _addUpdateFn(False, request, db_pool)


# To add/update an ProductCategory to the database
async def _addUpdateFn(toAdd, request:web_request.Request,db_pool:aioodbc.Pool):

    try:    
        data = await request.post()
        values = (data.get("name"),data.get('status'),data.get('vendorID'),data.get('menuID'),data.get('createdBy'))

        if not toAdd:
            values += (data.get("id"),)
            query = "UPDATE productCategory SET "
        else:
            query = "INSERT INTO productCategory "

        if toAdd:
            query += "(name, status,vendorID,menuID, createdBy) "
            query += "VALUES (?, ?,?, ?,?) "
        else:
            query += "name=?, status=?,vendorID=?menuID=?,createdBy=? WHERE id=?"
        
        async with db_pool.acquire() as cnxn:
            async with cnxn.cursor() as cursor:
                await cursor.execute(query, values)
                await cnxn.commit() 
        
        success_response = {
            "message": f"{'Added sccessfully' if toAdd else 'Updated successfully'}!"
        }
        return web.json_response(success_response, status=200)

    except Exception as e:
    # Catch specific exceptions and provide a more meaningful error response
        error_message = {"error": str(e)}
        return web.json_response(error_message, status=500)