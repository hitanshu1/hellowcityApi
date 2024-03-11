from ast import List
import json
import os
import aioodbc
from click import File
from ExceptionManager import mssqlExceptionManager
from aiohttp import web,web_request
from access_token import AccessToken
from apiResponse import ApiResponse
from products.productImage import uploadProductImages

# To add a vendor to the database
@AccessToken.token_required
async def addProduct(request, db_pool:aioodbc.Pool):
    return await _addUpdateFn(True, request, db_pool)


# To update a vendor from the database
@AccessToken.token_required
async def updateProduct(request, db_pool:aioodbc.Pool):
    return await _addUpdateFn(False, request, db_pool)


# To add/update an vendor to the database
async def _addUpdateFn(toAdd, request:web_request.Request,db_pool:aioodbc.Pool):

    try:    

        bodyData = await request.post()
        files = bodyData.getall('images')
        data_str =bodyData.get('data').decode('utf-8')
        data=json.loads(data_str)
                        
        values = (data.get("name"), data.get("shortName"), data.get("numberCode"), data.get("description"), data.get('vendorID'),
          data.get("categoryID"), data.get("adminCategoryID"), data.get("isDigital"), data.get("isTakeAway"), data.get("regularPrice"),
          data.get('discountPrice'), data.get('quantity'), data.get('availableQuantity'), data.get('type'),
          data.get('createdBy'), data.get('updatedBy'), data.get('calories'),
          data.get('grams'), data.get('proteins'), data.get('fats'), data.get('brandID'),
        data.get('saleType'), data.get('subType'),data.get('status'),data.get('updatedAt'))

        if not toAdd:
            values += (data.get("id"),)
            query = "UPDATE product SET "
        else:
            query = "INSERT INTO product "

        if toAdd:
            query += "(name, shortName, numberCode, description, vendorID, categoryID, adminCategoryID, isDigital, isTakeAway, regularPrice, discountPrice, quantity, availableQuantity, type, createdBy, updatedBy, calories, grams, proteins, fats, brandID,  saleType,subType, status,updatedAt) "
            query += "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?) "
        else:
            query += "name=?, shortName=?, numberCode=?, description=?, vendorID=?, categoryID=?, adminCategoryID=?, isDigital=?, isTakeAway=?, regularPrice=?, discountPrice=?, quantity=?, availableQuantity=?, type=?, createdBy=?, updatedBy=?, calories=?, grams=?, proteins=?, fats=?, brandID=?, saleType=?, subType=?,status=?,updatedAt=? WHERE id=?"
        
        async with db_pool.acquire() as cnxn:
            async with cnxn.cursor() as cursor:
                await cursor.execute(query, values)
                await cnxn.commit() 
                await cursor.execute("SELECT @@IDENTITY")
                row = await cursor.fetchone()
                if row:
                    inserted_id = row[0]
                    files = list(filter(lambda x: x != '', files))
                    if files is not None:
                        await uploadProductImages(files=files,productID=inserted_id,db_pool=db_pool)
        
        success_response =  f"{'Added sccessfully' if toAdd else 'Updated successfully'}!"
        
        return ApiResponse.message(True,{},success_response)
    except Exception as e:
    # Catch specific exceptions and provide a more meaningful error response
        error_message = {"error": str(e)}
        return ApiResponse.message(False,{},error_message)
