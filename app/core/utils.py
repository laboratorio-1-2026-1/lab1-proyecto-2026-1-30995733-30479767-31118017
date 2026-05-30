from sqlalchemy.orm import Session
import math
from app.core.exceptions import BadRequestException

def paginar_resultados(db: Session, crud_repo, page: int, page_size: int, query_personalizada=None):

    if page < 1 or page_size < 1:
        raise BadRequestException(
            codigo_interno="ERR_PAGINACION_INVALIDA",
            mensaje="Los parámetros de página deben ser mayores a 0."
        )

    query = query_personalizada if query_personalizada is not None else db.query(crud_repo.model)
    
    total_rows = query.count()
    total_pages = math.ceil(total_rows / page_size) if total_rows > 0 else 1
    skip = (page - 1) * page_size
    rows = query.offset(skip).limit(page_size).all()
    
    return {
        "meta": {
            "total_rows": total_rows, 
            "current_page": page, 
            "page_size": page_size, 
            "total_pages": total_pages
        },
        "rows": rows
    }