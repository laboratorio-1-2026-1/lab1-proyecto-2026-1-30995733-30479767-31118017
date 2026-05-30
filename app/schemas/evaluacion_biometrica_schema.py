from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.schemas.paginacion_schema import PaginatedMeta

class EvaluacionBiometricaBase(BaseModel):
    id_cliente: int
    id_entrenador: int
    peso: float
    altura: float
    porc_grasa: float
    observaciones: Optional[str] = None
    historial: Optional[str] = None
    fecha: datetime

class EvaluacionBiometricaCreate(EvaluacionBiometricaBase):
    pass

class EvaluacionBiometricaResponse(EvaluacionBiometricaBase):
    id_evaluacion: int

    class Config:
        from_attributes = True

class EvaluacionBiometricaPaginatedResponse(BaseModel):
    meta: PaginatedMeta
    rows: List[EvaluacionBiometricaResponse]

class EvaluacionBiometricaUpdate(BaseModel):
    peso: Optional[float] = None
    altura: Optional[float] = None
    porc_grasa: Optional[float] = None
    observaciones: Optional[str] = None
    historial: Optional[str] = None