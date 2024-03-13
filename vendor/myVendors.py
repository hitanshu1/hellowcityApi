import json
import aioodbc
from ExceptionManager import mssqlExceptionManager
from aiohttp import web,web_request
import hashlib

from access_token import AccessToken
from apiResponse import ApiResponse
from vendor.schema import VendorSchema


@AccessToken.token_required

async def getMyVendors(request:web_request.Request, db_pool:aioodbc.Pool):
    try:   
    
        id = request.query.get("id")  # Assuming id comes from the request
        myVendors=[]

    
    # Construct the SQL query
        query = f"SELECT * FROM vendor WHERE authorID = {id}"
    
        async with db_pool.acquire() as cnxn:
            async with cnxn.cursor() as cursor:
                await cursor.execute(query)
                rows = await cursor.fetchall()
                if rows:
                    columns = [column[0] for column in cursor.description]
                    for row in rows:
                        item_dic = dict(zip(columns, row))
                        vendor_schema = VendorSchema()
                        try:
                            vendor_data = vendor_schema.load(item_dic)
                            serialized_data = vendor_schema.dump(vendor_data)
                            serialized_data['userType']='AUTHOR'
                            myVendors.append(serialized_data)
                        except Exception as e:
                            return ApiResponse.message(False, {}, str(e))
                    
                # return ApiResponse.message(True,result)
        
        query2 = f"SELECT * FROM stuff WHERE userID = {id}"
    
        async with db_pool.acquire() as cnxn:
            async with cnxn.cursor() as cursor:
                await cursor.execute(query2)
                rows = await cursor.fetchall()
                if rows:
                    columns = [column[0] for column in cursor.description]
                    for row in rows:
                        stuffDic = dict(zip(columns, row))
                        vendoID=stuffDic['vendorID']
                        query3 = f"SELECT * FROM vendor WHERE id = {vendoID}"
                        await cursor.execute(query3)
                        row = await cursor.fetchone()
                        columns = [column[0] for column in cursor.description]
                        if row:
                            vendor_dic = dict(zip(columns, row))
                            vendor_schema = VendorSchema()
                            vendor_data = vendor_schema.load(vendor_dic)
                            serialized_data = vendor_schema.dump(vendor_data)
                            serialized_data['userType']=stuffDic['userType']  
                            myVendors.append(serialized_data)
                    
        
        return ApiResponse.message(True,myVendors)


    except Exception as e:
    # Catch specific exceptions and provide a more meaningful error response
        error_message = {"status":0,"error": str(e)}
        return ApiResponse.message(False,{},str(e))