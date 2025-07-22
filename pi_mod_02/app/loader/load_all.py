from app.db.session import SessionLocal
from app.loader.base import DataLoader

import app.loader.user_loader
import app.loader.category_loader
import app.loader.product_loader
import app.loader.order_loader
import app.loader.orders_detail_loader
import app.loader.delivery_address_loader
import app.loader.cart_loader
import app.loader.payment_method_loader
import app.loader.order_payment_method_loader
import app.loader.reviews_loader
import app.loader.payment_history_loader


def run_all_table_loaders():
    db = SessionLocal()

    for LoaderClass in sorted(DataLoader._registry, key=lambda cls: cls.priority):
        print(f"Ejecutando loader: {LoaderClass.__name__}")
        loader = LoaderClass()
        loader.run(db)

    db.commit()
    db.close()
    print("Carga completa de datos.")


if __name__ == "__main__":
    run_all_table_loaders()
