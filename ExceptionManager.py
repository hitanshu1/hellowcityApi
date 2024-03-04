import re
from aiohttp import web


async def mssqlExceptionManager(e):
    print(f"MSSQL ACTUAL EXCEPTION: {e}")

    try:
        error_string = str(e)
        errorCode_match = re.search(r"\((\d+)\)", error_string)
        errorMessage_match = re.search(r"\[SQL Server\](.+?)\(\d+\)", error_string)

        if errorCode_match:
            print("errorCode_matched")
            errorCode = errorCode_match.group(1)
            errorCode = int(errorCode[-3:])
        else:
            print("errorCode not matched so setting as 500")
            errorCode = 500

        if errorMessage_match:
            print("errorMessage matched")
            errorMessage = errorMessage_match.group(1)
        else:
            print("errorMessage not matched so setting a db error message")
            errorMessage = "Something went wrong in database!"

        error_response = {"error": str(errorMessage)}
        print(f"errorCode: ${errorCode}: errorMessage {errorMessage}")
        return web.json_response(error_response, status=errorCode)

    except Exception as e:
        # Handle any further exceptions gracefully or log them
        error_response = {"error": "Internal server error"}
        return web.json_response(error_response, status=500)
