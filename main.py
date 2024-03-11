"""
Web Server Application using aiohttp for handling HTTP requests and aioodbc for database connections.
"""

import aioodbc
from aiohttp import web
import threading
import aiohttp_cors
import config
from setupRoutes import routes


class DatabasePool:
    """
    A class to manage the database connection pool.

    Attributes:
        dsn (str): The Data Source Name (DSN) for the database connection.
        pool (aioodbc.Pool): A database connection pool.
    """

    def __init__(self, dsn):
        """
        Initializes a DatabasePool instance.

        Args:
            dsn (str): The Data Source Name (DSN) for the database connection.
        """
        self.dsn = dsn
        self.pool = None

    async def init_pool(self):
        """
        Creates a database connection pool during application startup.
        """
        self.pool = await aioodbc.create_pool(dsn=self.dsn)
    
    

    async def close_pool(self):
        """
        Closes the database connection pool.
        """
        if self.pool is not None:
            self.pool.close()
            await self.pool.wait_closed()


# Create a web application instance
app = web.Application()


# Configure CORS using aiohttp-cors
cors = aiohttp_cors.setup(
    app,
    defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            
        )
    },
)

# Add the CORS middleware before any other middleware or routes
# app.middlewares.append(cors_middleware)

# Define a Data Source Name (DSN) for the database connection
dsn = config.connection


async def on_startup(app):
    """
    Function to be executed during application startup.
    It initializes the database connection pool and stores it in the application's context.

    Args:
        app (web.Application): The web application instance.
    """
    db_pool = DatabasePool(dsn)
    try:
        await db_pool.init_pool()
        app["db_pool"] = db_pool
    except Exception as e:
        print(f"Error initializing the database pool: {e}")
        raise web.HTTPInternalServerError() from e


async def on_cleanup(app):
    """
    Function to be executed during application cleanup.
    It closes the database connection pool if it exists.

    Args:
        app (web.Application): The web application instance.
    """
    db_pool = app.get("db_pool")
    if db_pool:
        try:
            await db_pool.close_pool()
        except Exception as e:
            print(f"Error closing the database pool: {e}")


app.on_startup.append(on_startup)
app.on_cleanup.append(on_cleanup)


def http_method(methods):
    """
    Custom decorator to specify allowed HTTP methods for a handler.

    Args:
        methods (list): List of allowed HTTP methods (e.g., ['GET', 'POST']).

    Returns:
        callable: Decorator function.
    """

    def decorator(handler):
        async def wrapped(request, pool):
            if request.method in methods:
                # Call the handler function for the specified HTTP method
                return await handler(request, pool)
            else:
                # Return a "Method Not Allowed" response for unsupported methods
                return web.Response(status=405)

        return wrapped

    return decorator


for route, route_config in routes.items():
    handler = route_config["handler"]
    methods = route_config["methods"]

    for method in methods:
        # Add routes with associated handlers
        cors.add(
            app.router.add_route(
                method, route, lambda r, h=handler: h(r, app["db_pool"].pool)
            )
        )
        # app.router.add_route(method, route, lambda r, h=handler: h(r, app['db_pool']))


def run_server():
    try:
        web.run_app(app, host=config.HOST, port=config.PORT)
    except OSError as e:
        print(f"Error starting the server: {e}")


if __name__ == "__main__":
    run_server()


# Start the server
if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
    server_thread.join()
