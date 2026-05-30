from fastapi import HTTPException
from datetime import datetime, timezone

class SmartGymException(HTTPException):

    def __init__(self, error_type: str, status_code: int, codigo_interno: str, mensaje: str):
        self.error_type = error_type
        self.codigo_interno = codigo_interno
        self.mensaje = mensaje
        self.timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        detalle_error = {
            "error_type": self.error_type,
            "status_code": status_code,
            "codigo_interno": self.codigo_interno,
            "mensaje": self.mensaje,
            "timestamp": self.timestamp
        }
        super().__init__(status_code=status_code, detail=detalle_error)

class BadRequestException(SmartGymException):
    def __init__(self, codigo_interno: str, mensaje: str):
        super().__init__(
            error_type="Bad Request",
            status_code=400,
            codigo_interno=codigo_interno,
            mensaje=mensaje
        )

class ConflictException(SmartGymException):
    def __init__(self, codigo_interno: str, mensaje: str):
        super().__init__(
            error_type="Conflict",
            status_code=409,
            codigo_interno=codigo_interno,
            mensaje=mensaje
        )

class NotFoundException(SmartGymException):
    def __init__(self, codigo_interno: str, mensaje: str):
        super().__init__(
            error_type="Not Found",
            status_code=404,
            codigo_interno=codigo_interno,
            mensaje=mensaje
        )