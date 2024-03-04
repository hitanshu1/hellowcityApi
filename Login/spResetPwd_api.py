import aioodbc
from ExceptionManager import mssqlExceptionManager


# Toupdate password
async def update_pwd(request, db_pool:aioodbc.Pool):
    try:
        data = await request.json()
        # Validate that "ID" and "newPassword" fields exist in the JSON data
        if "ID" not in data or "newPassword" not in data:
            error_message = {"error": "Both ID and newPassword fields are required."}
            return web.Response(
                text=json.dumps(error_message),
                status=400,
                content_type="application/json",
            )

        ID = data.get("ID")
        newPassword = data.get("newPassword")

        # Validate the format or content of "ID" and "newPassword" as needed
        if not ID or not newPassword:
            error_message = {
                "error": "Both ID and newPassword fields must have non-empty values."
            }
            return web.Response(
                text=json.dumps(error_message),
                status=400,
                content_type="application/json",
            )
        data = await request.json()

        query = "EXEC [dbo].[spResetPwd] ?,?"
        params = (ID, newPassword)

        async with db_pool.acquire() as cnxn:
            async with cnxn.cursor() as cursor:
                await cursor.execute(query, params)
                await cnxn.commit()

        response = {"message": "newPassword updated successfully"}

        return web.json_response(response)

    except Exception as e:
        return await mssqlExceptionManager(e)


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from aiohttp import web
import json


# Asynchronous function to request a password reset
async def request_reset_password(request, db_pool:aioodbc.Pool):
    try:
        data = await request.json()
        # Validate that "ID" field exist in the JSON data
        if "ID" not in data:
            error_message = {"error": "ID field is required."}
            return web.Response(
                text=json.dumps(error_message),
                status=400,
                content_type="application/json",
            )

        ID = data.get("ID")

        # Validate the format or content of "ID" as needed
        if not ID:
            error_message = {"error": "ID field is empty."}
            return web.Response(
                text=json.dumps(error_message),
                status=400,
                content_type="application/json",
            )

        # Execute the stored procedure to generate a token
        query = "DECLARE @Token NVARCHAR(255);EXEC [dbo].[GeneratePwdToken] ?, @Token OUTPUT;"
        params = (ID,)

        async with db_pool.acquire() as cnxn:
            async with cnxn.cursor() as cursor:
                await cursor.execute(query, params)
                row = await cursor.fetchone()

        if row is not None:
            reset_token = row[
                0
            ]  # Extract the token value from the first column of the row
        else:
            reset_token = None

        # Send the reset link to the user via email
        send_reset_link_email(ID, reset_token)

        response = {"message": "Password reset link sent successfully"}
        return web.json_response(response)

    except Exception as e:
        error_response = {"error": str(e)}
        return web.json_response(error_response, status=500)


# Function to send reset link via email
def send_reset_link_email(ID, reset_token):
    # Email configuration (use your own email and SMTP server settings)
    sender_email = "fms.cool16@gmail.com"
    sender_password = "dyfr cqqt ecpt qwzj"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Email subject and body with the reset link
    subject = "Password Reset Link"
    reset_link = f"https://solverpayroll.web.app//reset_password?token={reset_token}"
    body = f"Click the following link to reset your password: {reset_link}"

    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ID
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Connect to the SMTP server and send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, ID, message.as_string())
        print(f"Password reset link sent to {ID} via email.")
    except Exception as e:
        print(f"Error sending email: {str(e)}")
