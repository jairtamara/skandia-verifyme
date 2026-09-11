from pydantic import BaseModel
from typing import Optional


class Cliente(BaseModel):
    id: str
    nombre: str
    email: str
    telefono: Optional[str] = None
    ciudad: Optional[str] = None
    actualizado_en: Optional[str] = None


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    ciudad: Optional[str] = None


class ResultadoMetaSimulado(BaseModel):
    encontrado: bool
    email: str
    usuario_instagram: Optional[str] = None
    usuario_facebook: Optional[str] = None
    seguidores: Optional[int] = None
    ciudad_red_social: Optional[str] = None
    perfil_url: Optional[str] = None
