from fastapi import APIRouter, HTTPException, Response, status
from app.services.data_load_service import DataLoadService
router = APIRouter()

CSV_DIRECTORY = "/app/csv_data"  


@router.post("/load-csvs", status_code=status.HTTP_201_CREATED)
def load_csvs():
    """
    Carga todos los archivos CSV del directorio en sus respectivas tablas.
    """
    return {"message": "Endpoint de carga de CSVs está en construcción."}
    # data_load_service = DataLoadService()

    # try:
    #     for filename in os.listdir(CSV_DIRECTORY):
    #         if filename.endswith(".csv"):
    #             csv_file_path = os.path.join(CSV_DIRECTORY, filename)
    #             table_name = filename.split(".")[0]
    #             print(f"Iniciando carga de: {csv_file_path}, en {table_name}")

    #             data_load_service.load_csv_to_db(csv_file_path, table_name)

    #     return {"message": "Carga de todos los archivos CSV completada!!!"}

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Error durante la carga: {str(e)}")
