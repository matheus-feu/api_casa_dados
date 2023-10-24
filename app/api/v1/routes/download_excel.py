import os

from fastapi import APIRouter, HTTPException
from starlette.responses import StreamingResponse

router = APIRouter()


@router.get("/download_excel/{endpoint}", summary="Download excel")
async def download_excel(endpoint: str):
    """
    Download do arquivo excel gerado pelo scraping,
    informar o endpoint que deseja realizar o download se é basic_search ou advanced_search.
    """

    file_path = os.path.join("excel", f"{endpoint}.xlsx")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="O arquivo não foi encontrado.")

    try:
        return StreamingResponse(
            open(file_path, 'rb'),
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={'Content-Disposition': f'attachment; filename={endpoint}.xlsx'}
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Não foi possível realizar o download do arquivo.")
