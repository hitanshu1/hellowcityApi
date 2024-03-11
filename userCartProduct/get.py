import json
import aioodbc
from ExceptionManager import mssqlExceptionManager
from aiohttp import web,web_request
from access_token import AccessToken
from apiResponse import ApiResponse
from userCartProduct.schema import CartProductSchema


@AccessToken.token_required

async def getUserCartProducts(request:web_request.Request, db_pool:aioodbc.Pool):
    try:   
        
            userID =request.query.get('userID')
            query = f"SELECT * FROM userCartProduct WHERE userID = {userID}"
            async with db_pool.acquire() as cnxn:
                async with cnxn.cursor() as cursor:
                    await cursor.execute(query)
                    rows = await cursor.fetchall()
                    result = []
                    if rows:
                        columns = [column[0] for column in cursor.description]
                        result = []
                        for row in rows:
                            item_dic = dict(zip(columns, row))
                            cartProductSchema = CartProductSchema()
                            try:
                                vendor_data = cartProductSchema.load(item_dic)
                                serialized_data = cartProductSchema.dump(vendor_data)
                                result.append(serialized_data)
                            except Exception as e:
                                return ApiResponse.message(False, {}, str(e))
                    
                    return ApiResponse.message(True,result)


    except Exception as e:
    # Catch specific exceptions and provide a more meaningful error response
        error_message = {"status":0,"error": str(e)}
        return ApiResponse.message(False,{},str(e))