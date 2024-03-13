from Files.Upload import uploadFileFn
from appSettings.addUpdate import addAppSetting, updateAppSetting
from appSettings.get import getAppSettings
from offer.addUpdate import addOfferFn, updateOfferFn
from offer.delete import deleteOffer
from offer.get import getOffer
from orders.addUpdate import addOrder, updateOrder
from orders.delete import deleteOrder
from orders.get import getOrders
from ping import pingFn
from Login.login import loginFn
from Login.spResetPwd_api import update_pwd
from Login.spResetPwd_api import request_reset_password
from products.addUpdate import addProduct, updateProduct
from products.delete import deleteProduct
from products.get import getProduct
from productCategory.addUpdate import addProductCategory, updateProductCategory
from productCategory.delete import deleteProductCategory
from productCategory.get import getProductCategory
from productMenu.addUpdate import addProductMenu, updateProductMenu
from productMenu.delete import deleteProductMenu
from productMenu.get import getProductMenu
from stuff.addUpdate import addStuffFn, updateStuffFn
from stuff.get import getStuff
from userCartProduct.addUpdate import addProductToCart, updateProductOfCart
from userCartProduct.delete import deleteAllCartProduct
from userCartProduct.get import getUserCartProducts
from users.addUpdate import addRegistrationFn, updateRegistrationFn
from users.get import getUsers
from vendor.addUpdate import addVendor, updateVendor
from vendor.delete import deleteVendor
from vendor.get import getVendor
from vendor.myVendors import getMyVendors
from vendorCategory.addUpdate import addVendorCategory, updateVendorCategory
from vendorCategory.delete import deleteVendorCategory
from vendorCategory.get import getVendorCategory

# Define a dictionary to map routes to their handlers and allowed methods
routes = {
    # Connection check
    "/": {
        "handler": pingFn,
        "methods": ["GET"],
    },
     "/api/getUsers": {
        "handler": getUsers,
        "methods": ["GET"],
    },
    # '/': {'handler': partial(check_connection, db_pool=app['db_pool']), 'methods': ['GET'],},
    "/api/login": {
        "handler": loginFn,
        "methods": ["POST"],
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
    "/api/updateRegistration": {
        "handler": updateRegistrationFn,
        "methods": ["PUT"],
    },
    "/api/addVendor": {
        "handler": addVendor,
        "methods": ["POST"],
    },
    "/api/updateVendor": {
        "handler": updateVendor,
        "methods": ["PUT"],
    },
    "/api/getMyVendors": {
        "handler": getMyVendors,
        "methods": ["GET"],
    },
    "/api/getVendor": {
        "handler": getVendor,
        "methods": ["GET"],
    },
    "/api/deleteVendor": {
        "handler": deleteVendor,
        "methods": ["DELETE"],
    },
     "/api/addVendorCategory": {
        "handler": addVendorCategory,
        "methods": ["POST"],
    },
    "/api/updateVendorCategory": {
        "handler": updateVendorCategory,
        "methods": ["PUT"],
    },
    "/api/getVendorCategory": {
        "handler": getVendorCategory,
        "methods": ["GET"],
    },
    "/api/deleteVendorCategory": {
        "handler": deleteVendorCategory,
        "methods": ["DELETE"],
    },
     "/api/addProductCategory": {
        "handler": addProductCategory,
        "methods": ["POST"],
    },
    "/api/updateProductCategory": {
        "handler": updateProductCategory,
        "methods": ["PUT"],
    },
    "/api/getProductCategory": {
        "handler": getProductCategory,
        "methods": ["GET"],
    },
    "/api/deleteProductCategory": {
        "handler": deleteProductCategory,
        "methods": ["DELETE"],
    },
     "/api/addProduct": {
        "handler": addProduct,
        "methods": ["POST"],
    },
    "/api/updateProduct": {
        "handler": updateProduct,
        "methods": ["PUT"],
    },
    "/api/getProduct": {
        "handler": getProduct,
        "methods": ["GET"],
    },
    "/api/deleteProduct": {
        "handler": deleteProduct,
        "methods": ["DELETE"],
    },
     "/api/addOrder": {
        "handler": addOrder,
        "methods": ["POST"],
    },
    "/api/updateOrder": {
        "handler": updateOrder,
        "methods": ["PUT"],
    },
    "/api/getOrder": {
        "handler": getOrders,
        "methods": ["GET"],
    },
    "/api/deleteOrder": {
        "handler": deleteOrder,
        "methods": ["DELETE"],
    },
     "/api/addOffer": {
        "handler": addOfferFn,
        "methods": ["POST"],
    },
    "/api/updateOffer": {
        "handler": updateOfferFn,
        "methods": ["PUT"],
    },
    "/api/getOffer": {
        "handler": getOffer,
        "methods": ["GET"],
    },
    "/api/deleteOrder": {
        "handler": deleteOffer,
        "methods": ["DELETE"],
    },
    "/api/addProductMenu": {
        "handler": addProductMenu,
        "methods": ["POST"],
    },
    "/api/updateProductMenu": {
        "handler": updateProductMenu,
        "methods": ["PUT"],
    },
    "/api/getProductMenu": {
        "handler": getProductMenu,
        "methods": ["GET"],
    },
    "/api/deleteProductMenu": {
        "handler": deleteProductMenu,
        "methods": ["DELETE"],
    },

    "/api/addProductToCart": {
        "handler": addProductToCart,
        "methods": ["POST"],
    },
    "/api/updateProductOfCart": {
        "handler": updateProductOfCart,
        "methods": ["PUT"],
    },
    "/api/getUserCartProducts": {
        "handler": getUserCartProducts,
        "methods": ["GET"],
    },
    "/api/deleteAllCartProduct": {
        "handler": deleteAllCartProduct,
        "methods": ["DELETE"],
    },
    "/api/addAppSetting": {
        "handler": addAppSetting,
        "methods": ["POST"],
    },
    "/api/updateAppSetting": {
        "handler": updateAppSetting,
        "methods": ["PUT"],
    },
    "/api/getAppSettings": {
        "handler": getAppSettings,
        "methods": ["GET"],
    },
    "/api/addStuff": {
        "handler": addStuffFn,
        "methods": ["POST"],
    },
    "/api/updateStuff": {
        "handler": updateStuffFn,
        "methods": ["PUT"],
    },
    "/api/getStuff": {
        "handler": getStuff,
        "methods": ["GET"],
    },

}
