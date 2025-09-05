from app.stage.scripts.populate_dim_tables import populate_dim_tables  # si aplica


def stagging_data():
    populate_dim_tables()

    print("Proceso de ETL completado.")


if __name__ == "__main__":
    stagging_data()
