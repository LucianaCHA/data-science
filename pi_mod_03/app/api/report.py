from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from app.services.cloud_storage.cloud_storage import GCSService
from app.config.config import Settings

router = APIRouter()


settings = Settings()
REPORTS_PREFIX = "analitics_reports_html/"
gcs_service = GCSService(bucket_name=settings.GCS_BUCKET)


@router.get("/", response_class=HTMLResponse)
def get_latest_report():
    try:
        gcs = GCSService(bucket_name=settings.GCS_BUCKET)
        blobs = list(gcs.list_blobs(prefix=REPORTS_PREFIX))

        if not blobs:
            raise HTTPException(status_code=404, detail="No hay reportes disponibles.")

        latest_blob = max(blobs, key=lambda b: b.updated)
        html_content = latest_blob.download_as_text()
        return HTMLResponse(content=html_content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
