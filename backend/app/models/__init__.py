from __future__ import annotations
from app.database import Base
from app.models.condominio import Condominio
from app.models.apartamento import Apartamento
from app.models.morador import Morador
from app.models.ocorrencia import Ocorrencia
from app.models.rivalidade import Rivalidade

__all__ = [
    "Base",
    "Condominio",
    "Apartamento",
    "Morador",
    "Ocorrencia",
    "Rivalidade",
]
