from Files.Upload import uploadFileFn
from ping import pingFn
from Login.login import loginFn
from Login.spResetPwd_api import update_pwd
from Login.spResetPwd_api import request_reset_password

# from Staffs.delete import deleteStaffFn
from Registrations.addUpdate import addRegistrationFn, updateRegistrationFn
from Registrations.get import searchRegistrationsFn

# Define a dictionary to map routes to their handlers and allowed methods
routes = {
    # Connection check
    "/": {
        "handler": pingFn,
        "methods": ["GET"],
    },
    # '/': {'handler': partial(check_connection, db_pool=app['db_pool']), 'methods': ['GET'],},
    "/api/login": {
        "handler": loginFn,
        "methods": ["GET"],
    },

    "/api/updatePwd": {
        "handler": update_pwd,
        "methods": ["POST"],
    },
    "/api/resetPwd": {
        "handler": request_reset_password,
        "methods": ["POST"],
    },
   
    "/api/upload": {
        "handler": uploadFileFn,
        "methods": ["POST"],
    },
    "/api/addRegistration": {
        "handler": addRegistrationFn,
        "methods": ["POST"],
    },
    "/api/updateRegistration": {
        "handler": updateRegistrationFn,
        "methods": ["PUT"],
    },

}
