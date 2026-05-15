from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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