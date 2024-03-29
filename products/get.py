from decimal import Decimal
import json
import aioodbc
from ExceptionManager import mssqlExceptionManager
from aiohttp import web,web_request
from access_token import AccessToken
from apiResponse import ApiResponse
from products.schema import ProductSchema


@AccessToken.token_required
async def getProduct(request:web_request.Request, db_pool:aioodbc.Pool):
    try:   
        id =request.query.get('id')
        if id is not None:
            query = f"SELECT * FROM product WHERE id = {id}"
            async with db_pool.acquire() as cnxn:
                async with cnxn.cursor() as cursor:
                    await cursor.execute(query)
                    row = await cursor.fetchone()
                    columns = [column[0] for column in cursor.description]
                    if row:
                        item_dic = dict(zip(columns, row))
                        product_schema = ProductSchema()
                        try:
                            user_data = product_schema.load(item_dic)
                            serialized_data = product_schema.dump(user_data)
                            return ApiResponse.message(True, serialized_data)
                        except Exception as e:
                            return ApiResponse.message(False, {}, str(e))
                    else:
                        return ApiResponse.message(False, {}, "No result found")
        else:
            Offset = int(request.query.get("offset") or 0)
            Limit = int(request.query.get("limit") or 50)
            query = f"SELECT * FROM product ORDER BY id OFFSET {Offset} ROWS FETCH NEXT {Limit} ROWS ONLY"
        

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
                            product_schema = ProductSchema()
                            try:
                                user_data = product_schema.load(item_dic)
                                serialized_data = product_schema.dump(user_data)
                                result.append(serialized_data)
                            except Exception as e:
                                return ApiResponse.message(False, {}, str(e))
                    
                    return ApiResponse.message(True,result)


    except Exception as e:
    # Catch specific exceptions and provide a more meaningful error response
        error_message = {"status":0,"error": str(e)}
        return ApiResponse.message(False,{},str(e))