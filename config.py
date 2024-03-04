import pyodbc

DRIVER = "ODBC Driver 17 for SQL Server"
UID = "sa"
PWD = "Capital123Small"
SERVER = "localhost"
DATABASE = "Hellowcity"

# Connection String used to connect to the sql database, which is running either on localhost or online
connection = f"DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};UID={UID};PWD={PWD}"

# ODBC driver is connecting to the sql database
conn = pyodbc.connect(connection)
cursor = conn.cursor()
# Port where this python server has to run
PORT = 5000
# Host ip where the python server has to run. [0.0.0.0] means [localhost]
HOST = "localhost"
# To close the connection when the server responded to a http request.
conn.close()
