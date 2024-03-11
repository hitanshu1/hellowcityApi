import aioodbc
from ExceptionManager import mssqlExceptionManager
from aiohttp import web,web_request
import hashlib

from extension.datetimeEx import to_datetime

# To add a offer to the database
async def addOfferFn(request, db_pool:aioodbc.Pool):
    return await _addUpdateFn(True, request, db_pool)


# To update a offer from the database
async def updateOfferFn(request, db_pool:aioodbc.Pool):
    return await _addUpdateFn(False, request, db_pool)


# To add/update an offer to the database
async def _addUpdateFn(toAdd, request:web_request.Request,db_pool:aioodbc.Pool):

    try:    
        data = await request.post()
      
        values = (data.get("title"), data.get("description"), data.get("type"), data.get("status"),data.get("vendorID"),
                  to_datetime(data.get("startDate")),to_datetime(data.get("endDate")),to_datetime(data.get("updatedAt")))
        
        if not toAdd:
            values += (data.get("id"),)
            query = "UPDATE offer SET "
        else:
            query = "INSERT INTO offer "

        if toAdd:
            
            query += "(title, description, type, status,vendorID, startDate, endDate,updatedAt) "
            query += "VALUES (?, ?, ?, ?, ?, ?, ?,?) "
        else:
            query += "title=?, description=?, type=?, status=?, vendorID=?, startDate=?, endDate=?, updatedAt=? WHERE id=?"
        
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