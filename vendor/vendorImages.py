
import os
import uuid
import aioodbc


async def uploadVendorImages(files, vendorID: int, db_pool: aioodbc.Pool):
    try:
        # Define the upload directory (C:\hellowcity_file_storage)
        # Use 'r' prefix for raw string to handle backslashes
        upload_dir = r"file_storage"
        # Create the upload directory if it doesn't exist
        os.makedirs(upload_dir, exist_ok=True)
        
        for file in files:
            filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[-1]
            filepath = os.path.join(upload_dir, filename)
            # Write the file
            with open(filepath, "wb") as f:
                while True:
                    chunk = file.file.read()
                    if not chunk:
                        break
                    f.write(chunk)
            print(f"File saved at: {filepath}")

            # Insert the file path into the database
            query = "INSERT INTO vendorImage (vendorID, type, image) VALUES (?, ?, ?);"
            values = (vendorID, 'product', filename)
            
            async with db_pool.acquire() as cnxn:
                async with cnxn.cursor() as cursor:
                    await cursor.execute(query, values)
                    await cnxn.commit()  
                    

    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Return None if an error occur