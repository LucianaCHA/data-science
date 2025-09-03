from enum import StrEnum


class TableNames(StrEnum):
    USERS = "Usuarios"
    CATEGORIES = "Categorias"
    PRODUCTS = "Productos"
    ORDERS = "Ordenes"
    ORDER_DETAILS = "DetalleOrdenes"
    DELIVERY_ADDRESS = "DireccionesEnvio"
    CART = "Carrito"
    PAYMENT_METHODS = "MetodosPago"
    ORDERS_PAYMENT_METHODS = "OrdenesMetodosPago"
    REVIEWS = "ReseñasProductos"
    PAYMENT_HISTORY = "HistorialPagos"


class UserColumns(StrEnum):
    USER_ID = "UsuarioID"
    NAME = "Nombre"
    SURNAME = "Apellido"
    DNI = "DNI"
    EMAIL = "Email"
    PASSWORD = "Contraseña"
    REGISTRATION_DATE = "FechaRegistro"


class CategoryColumns(StrEnum):
    CATEGORY_ID = "CategoriaID"
    NAME = "Nombre"
    DESCRIPTION = "Descripcion"


class ProductColumns(StrEnum):
    PRODUCT_ID = "ProductoID"
    NAME = "Nombre"
    DESCRIPTION = "Descripcion"
    PRICE = "Precio"
    STOCK = "Stock"
    CATEGORY_ID = "CategoriaID"


class OrderColumns(StrEnum):
    ORDER_ID = "OrdenID"
    USER_ID = "UsuarioID"
    ORDER_DATE = "FechaOrden"
    TOTAL = "Total"
    STATUS = "Estado"


class OrderDetailColumns(StrEnum):
    ORDER_DETAIL_ID = "DetalleID"
    ORDER_ID = "OrdenID"
    PRODUCT_ID = "ProductoID"
    QUANTITY = "Cantidad"
    UNIT_PRICE = "PrecioUnitario"


class DeliveryAddressColumns(StrEnum):
    DELIVERY_ADDRESS_ID = "DireccionID"
    USER_ID = "UsuarioID"
    STREET = "Calle"
    CITY = "Ciudad"
    DEPARMENT = "Departamento"
    PROVINCE = "Provincia"
    DISTRICT = "Distrito"
    STATE = "Estado"
    ZIP_CODE = "CodigoPostal"
    COUNTRY = "Pais"


class CartColumns(StrEnum):
    CART_ID = "CarritoID"
    USER_ID = "UsuarioID"
    PRODUCT_ID = "ProductoID"
    QUANTITY = "Cantidad"
    ADDED_AT = "FechaAgregado"


class PaymentMethodColumns(StrEnum):
    PAYMENT_METHOD_ID = "MetodoPagoID"
    NAME = "Nombre"
    DESCRIPTION = "Descripcion"


class OrderPaymentMethodColumns(StrEnum):
    ORDER_PAYMENT_METHOD_ID = "OrdenMetodoID"
    ORDER_ID = "OrdenID"
    PAYMENT_METHOD_ID = "MetodoPagoID"
    AMOUNT_PAID = "MontoPagado"


class ProductReviewColumns(StrEnum):
    REVIEW_ID = "ReseñaID"
    PRODUCT_ID = "ProductoID"
    USER_ID = "UsuarioID"
    RATING = "Calificacion"
    COMMENT = "Comentario"
    REVIEW_DATE = "Fecha"


class PaymentHistoryColumns(StrEnum):
    PAYMENT_ID = "PagoID"
    ORDER_ID = "OrdenID"
    PAYMENT_METHOD_ID = "MetodoPagoID"
    AMOUNT = "Monto"
    PAYMENT_DATE = "FechaPago"
    PAYMENT_STATUS = "EstadoPago"
