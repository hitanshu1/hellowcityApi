from ast import List
import os
import aioodbc
from click import File
from ExceptionManager import mssqlExceptionManager
from aiohttp import web,web_request
from access_token import AccessToken

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
        data = await request.post()
        files = data.getall('images')
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
            query += "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?) "
        else:
            query += "name=?, shortName=?, numberCode=?, description=?, vendorID=?, categoryID=?, adminCategoryID=?, isDigital=?, isTakeAway=?, regularPrice=?, discountPrice=?, quantity=?, availableQuantity=?, type=?, createdBy=?, updatedBy=?, calories=?, grams=?, proteins=?, fats=?, brandID=?, saleType=?, subType=?,status=?,updatedAt=? WHERE id=?"
        
        async with db_pool.acquire() as cnxn:
            async with cnxn.cursor() as cursor:
                await cursor.execute(query, values)
                inserted_id = cursor.lastrowid
                await cnxn.commit() 
                if files is not None:
                    uploadFileAndGetPath(files=files,productID=inserted_id,db_pool=db_pool)
        
        success_response = {
            "message": f"{'Added sccessfully' if toAdd else 'Updated successfully'}!"
        }
        return web.json_response(success_response, status=200)

    except Exception as e:
    # Catch specific exceptions and provide a more meaningful error response
        error_message = {"error": str(e)}
        return web.json_response(error_message, status=500)
    


async def uploadFileAndGetPath(files: List[File], productID: int, db_pool: aioodbc.Pool):
    try:
        # Define the upload directory (C:\hellowcity_file_storage)
        # Use 'r' prefix for raw string to handle backslashes
        upload_dir = r"C:\hellowcity_file_storage"
        # Create the upload directory if it doesn't exist
        os.makedirs(upload_dir, exist_ok=True)
        
        for file in files:
            filename = file.filename
            filepath = os.path.join(upload_dir, filename)
            # Write the file
            with open(filepath, "wb") as f:
                while True:
                    chunk = await file.read_chunk()
                    if not chunk:
                        break
                    f.write(chunk)
            print(f"File saved at: {filepath}")

            # Insert the file path into the database
            query = "INSERT INTO users (productID, type, image) VALUES (?, ?, ?);"
            values = (productID, 'product', filepath)
            
            async with db_pool.acquire() as cnxn:
                async with cnxn.cursor() as cursor:
                    await cursor.execute(query, values)
                    await cnxn.commit() 
                    

    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Return None if an error occur