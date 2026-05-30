import time
import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GlobalMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        start_time = time.time()
        
        try:

            response = await call_next(request)
            
            process_time = (time.time() - start_time) * 1000
            
            logger.info(
                f"HTTP {request.method} {request.url.path} - "
                f"Status: {response.status_code} - Tiempo: {process_time:.2f}ms"
            )
            
            response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"
            return response
            
        except Exception as e:

            logger.error(f"Error inesperado en {request.url.path}: {str(e)}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Error interno del servidor, contacte al administrador."},
            )