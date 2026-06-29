from pydantic import BaseModel, EmailStr
from typing import Optional


class RemedioIn(BaseModel):
    nombre_remedio: str
    planta_base: Optional[str] = None
    propiedades: Optional[str] = None
    contraindicaciones: Optional[str] = None
    dosificacion: Optional[str] = None
    link_articulo_web: Optional[str] = None
    imagen_url: Optional[str] = None


class RemedioOut(RemedioIn):
    id_remedio: int


class UsuarioIn(BaseModel):
    nombre_completo: str
    celular: Optional[str] = None
    email: Optional[str] = None
    direccion_completa: Optional[str] = None
    ciudad_prov_pais: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None


class UsuarioOut(UsuarioIn):
    id_usuario: int
