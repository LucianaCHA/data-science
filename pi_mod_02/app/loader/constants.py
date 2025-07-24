from enum import StrEnum, IntEnum
import re

# USER_PRIORITY = 1
# CATEGORY_PRIORITY = 2


SQL_TO_USER_MODEL = {
    "Nombre": "name",
    "Apellido": "surname",
    "DNI": "dni",
    "Email": "email",
    "Contraseña": "password",
}

SQL_TO_CATEGORY_MODEL = {
    "Nombre": "name",
    "Descripcion": "description",
}

SQL_TO_PRODUCT_MODEL = {
    "Nombre": "name",
    "Descripcion": "description",
    "Precio": "price",
    "Stock": "stock",
    "CategoriaID": "category_id",
}

SQL_TO_ORDER_MODEL = {
    "UsuarioID": "user_id",
    "Fechaorden": "order_date",
    "Total": "total",
    "Estado": "status",
}

SQL_TO_ORDER_DETAIL_MODEL = {
    "OrdenID": "order_id",
    "ProductoID": "product_id",
    "Cantidad": "quantity",
    "PrecioUnitario": "unit_price",
}

SQL_TO_DELIVERY_ADDRESS_MODEL = {
    "UsuarioID": "user_id",
    "Calle": "street",
    "Ciudad": "city",
    "Departamento": "department",
    "Provincia": "province",
    "Distrito": "district",
    "Estado": "state",
    "CodigoPostal": "zip_code",
    "Pais": "country",
}

SQL_TO_CART_MODEL = {
    "UsuarioID": "user_id",
    "ProductoID": "product_id",
    "Cantidad": "quantity",
    "FechaAgregado": "added_at",
}

SQL_TO_PAYMENT_METHOD_MODEL = {
    "Nombre": "name",
    "Descripcion": "description",
}

SQL_TO_ORDERS_PAYMENT_METHOD_MODEL = {
    "OrdenID": "order_id",
    "MetodoPagoID": "payment_method_id",
    "MontoPagado": "amount_paid",
}
SQL_TO_PRODUCT_REVIEW_MODEL = {
    "UsuarioID": "user_id",
    "ProductoID": "product_id",
    "Calificacion": "rating",
    "Comentario": "comment",
    "Fecha": "date",
}
SQL_TO_PRODUCT_PAYMENT_HISTORY_MODEL = {
    "OrdenID": "order_id",
    "MetodoPagoID": "payment_method_id",
    "Monto": "amount",
    "FechaPago": "payment_date",
    "EstadoPago": "status",
}
