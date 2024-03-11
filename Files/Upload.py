from aiohttp import web
import os

import aioodbc
from click import File


# Function to upload a file into [C:/payroll_file_storage]
async def uploadFileFn(request):
    reader = await request.multipart()
    # Assuming 'file' is the name of the input field in the form
    field = await reader.next()
    filename = field.filename
    # Define the upload directory (C:\hellowcity_file_storage)
    # Use 'r' prefix for raw string to handle backslashes
    upload_dir = r"C:\hellowcity_file_storage"
    # Create the upload directory if it doesn't exist
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, filename)
    # Write the file
    with open(filepath, "wb") as f:
        while True:
            chunk = await field.read_chunk()
            if not chunk:
                break
            f.write(chunk)
            print(f"filePath: {filepath}")
    return web.json_response({"file_path": filepath})

async def uploadFileAndGetPath(file:File,imageType,db_pool:aioodbc.Pool):

    filename = file.filename
    # Define the upload directory (C:\hellowcity_file_storage)
    # Use 'r' prefix for raw string to handle backslashes
    upload_dir = r"C:\hellowcity_file_storage"
    # Create the upload directory if it doesn't exist
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, filename)
    # Write the file
    with open(filepath, "wb") as f:
        while True:
            chunk = await file.read_chunk()
            if not chunk:
                break
            f.write(chunk)
            print(f"filePath: {filepath}")

            query = "INSERT INTO users (type, image) VALUES (?, ?);"
            values = (imageType, filepath)
            async with db_pool.acquire() as cnxn:
                async with cnxn.cursor() as cursor:
                    await cursor.execute(query, values)
                    # Get the ID of the inserted record
                    inserted_id = cursor.lastrowid
                    await cnxn.commit() 
                    return inserted_id
