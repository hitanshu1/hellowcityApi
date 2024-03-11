import aioodbc
from ExceptionManager import mssqlExceptionManager
from aiohttp import web,web_request
import hashlib

from access_token import AccessToken
from apiResponse import ApiResponse

# To add a vendor to the database
@AccessToken.token_required
async def addProductToCart(request, db_pool: aioodbc.Pool):
    data = await request.post()
    userID = data.get('userID')
    productID = data.get('productID')
    vendorID = data.get('vendorID')
    
    query = f"SELECT * FROM userCartProduct WHERE userID = ? AND productID = ? AND vendorID = ?"
    async with db_pool.acquire() as cnxn:
        async with cnxn.cursor() as cursor:
            await cursor.execute(query, (userID, productID, vendorID))
            rows = await cursor.fetchall()
            rowCount = len(rows)
            if rowCount == 0:
                return await _addUpdateFn(True, request, db_pool)
            else:
                return ApiResponse.message(False, {}, "Product already added")


# To update a vendor from the database
@AccessToken.token_required
async def updateProductOfCart(request, db_pool:aioodbc.Pool):
    return await _addUpdateFn(False, request, db_pool)


# To add/update an vendor to the database
async def _addUpdateFn(toAdd, request:web_request.Request,db_pool:aioodbc.Pool):

    try:    
        data = await request.json()
        values = (data.get("userID"), 
                  data.get('productID'),data.get('quantity'),
                  data.get('vendorID'),
                  )

        if not toAdd:
            values += (data.get("id"),)
            query = "UPDATE userCartProduct SET "
        else:
            query = "INSERT INTO userCartProduct "
        
        if toAdd:
            query += "(userID,productID,quantity,vendorID) "
            query += "VALUES (?, ?, ?, ?) "
        else:
            query += "userID=?,vendorID=?,productID=?,quantity=? WHERE id=?"
        
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