import json
from typing import List, Set, Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI(
    title="API de Reformas",
    description="API para consultar proyectos de reforma.",
    version="1.0.0",
)

# modelos de datos

class Reforma(BaseModel):
    id: int
    archivo: str = Field(alias='file')
    titulo: str = Field(alias='title')
    presentador: str = Field(alias='presenter')
    proposito: str = Field(alias='purpose')
    beneficiarios: Union[str, List[str]] = Field(alias='beneficiaries')
    financiamiento: str = Field(alias='funding')
    categoria: str = Field(alias='category')

    @field_validator('beneficiarios', mode='before')
    def beneficiaries_to_str(cls, v):
        if isinstance(v, list):
            return ', '.join(map(str, v))
        return v

    class Config:
        populate_by_name = True

# carga de datos

def cargar_datos():
    try:
        with open("reformas.json", "r", encoding="utf-8") as f:
            datos_json = json.load(f)
        # Asignar un ID único a cada reforma
        return [Reforma(id=idx, **data) for idx, data in enumerate(datos_json)]
    except FileNotFoundError:
        return []

reformas: List[Reforma] = cargar_datos()

# funciones auxiliares

def buscar_por_campo(campo: str, valor: str) -> List[Reforma]:
    """Función genérica para filtrar reformas por un campo y valor."""
    valor_lower = valor.lower()
    return [r for r in reformas if getattr(r, campo).lower() == valor_lower]

def obtener_valores_unicos(campo: str) -> List[str]:
    """Función genérica para obtener valores únicos de un campo."""
    valores: Set[str] = {getattr(r, campo) for r in reformas}
    return sorted(list(valores))

# endpoints

@app.get("/api/estado", summary="Verificar estado de la API")
async def obtener_estado():
    """Devuelve el estado de salud de la API."""
    return {"estado": "ok"}

@app.get("/api/reformas", response_model=List[Reforma], summary="Obtener todas las reformas")
async def obtener_reformas():
    """Obtiene una lista de todos los proyectos de reforma."""
    return reformas

@app.get("/api/reforma/{reforma_id}", response_model=Reforma, summary="Obtener una reforma por ID")
async def obtener_reforma_por_id(reforma_id: int):
    """Obtiene un proyecto de reforma específico por su ID único."""
    try:
        return reformas[reforma_id]
    except IndexError:
        raise HTTPException(status_code=404, detail=f"Reforma con ID {reforma_id} no encontrada.")

@app.get("/api/reformas/buscar/{termino}", response_model=List[Reforma], summary="Buscar reformas por término")
async def buscar_reformas(termino: str):
    """
    Busca un término en los campos `titulo`, `proposito`, `presentador` y `categoria`.
    La búsqueda no distingue mayúsculas de minúsculas.
    """
    termino_lower = termino.lower()
    resultados = [
        r for r in reformas if
        termino_lower in r.titulo.lower() or
        termino_lower in r.proposito.lower() or
        termino_lower in r.presentador.lower() or
        termino_lower in r.categoria.lower()
    ]
    if not resultados:
        raise HTTPException(status_code=404, detail=f"No se encontraron reformas con el término '{termino}'.")
    return resultados

# endpoints de listas únicas

@app.get("/api/categorias", response_model=List[str], summary="Obtener lista de categorías")
async def obtener_categorias():
    return obtener_valores_unicos("categoria")

@app.get("/api/presentadores", response_model=List[str], summary="Obtener lista de presentadores")
async def obtener_presentadores():
    return obtener_valores_unicos("presentador")

@app.get("/api/beneficiarios", response_model=List[str], summary="Obtener lista de beneficiarios")
async def obtener_beneficiarios():
    return obtener_valores_unicos("beneficiarios")

@app.get("/api/financiamientos", response_model=List[str], summary="Obtener lista de tipos de financiamiento")
async def obtener_financiamientos():
    return obtener_valores_unicos("financiamiento")

# endpoints de filtrado

@app.get("/api/reformas/categoria/{valor}", response_model=List[Reforma], summary="Filtrar por categoría")
async def obtener_reformas_por_categoria(valor: str):
    resultados = buscar_por_campo("categoria", valor)
    if not resultados:
        raise HTTPException(status_code=404, detail=f"Categoría '{valor}' no encontrada.")
    return resultados

@app.get("/api/reformas/presentador/{valor}", response_model=List[Reforma], summary="Filtrar por presentador")
async def obtener_reformas_por_presentador(valor: str):
    resultados = buscar_por_campo("presentador", valor)
    if not resultados:
        raise HTTPException(status_code=404, detail=f"Presentador '{valor}' no encontrado.")
    return resultados

@app.get("/api/reformas/beneficiario/{valor}", response_model=List[Reforma], summary="Filtrar por beneficiario")
async def obtener_reformas_por_beneficiario(valor: str):
    resultados = buscar_por_campo("beneficiarios", valor)
    if not resultados:
        raise HTTPException(status_code=404, detail=f"Beneficiario '{valor}' no encontrado.")
    return resultados

@app.get("/api/reformas/financiamiento/{valor}", response_model=List[Reforma], summary="Filtrar por financiamiento")
async def obtener_reformas_por_financiamiento(valor: str):
    resultados = buscar_por_campo("financiamiento", valor)
    if not resultados:
        raise HTTPException(status_code=404, detail=f"Financiamiento '{valor}' no encontrado.")
    return resultados
