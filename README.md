# API de Proyectos de Reforma Constitucional de Santa Fe

Esta API fue creada para hacer accesibles los datos sobre los proyectos de reforma constitucional de la Provincia de Santa Fe, permitiendo que cualquier persona pueda usarlos para sus propias aplicaciones, investigaciones o simplemente para informarse.

La idea original y la recopilación de los PDFs fue de **[@martinv0x en X](https://x.com/martinv0x)**. Este proyecto busca expandir esa iniciativa y hacerla más accessible para desarrolladores y gente interesada en construir con esta API. La transparencia y el acceso público a la información son fundamentales.

## Cómo usarla localmente

Para probar la API seguí estos pasos en la terminal:

1.  **Navegá hasta la carpeta del proyecto:**
    ```bash
    cd /ruta/a/reformas/reformas
    ```

2.  **Creá y activá un entorno virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    *(Si al crearlo le pusiste otro nombre, como `vnev`, usá ese en el comando `source`)*

3.  **Instalá las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Iniciá el servidor:**
    ```bash
    uvicorn main:app --reload
    ```

Cuando esté activado y en ejecución, vas a poder acceder a la documentación interactiva desde `http://127.0.0.1:8000/docs`.

## Endpoints disponibles

### Generales

*   `GET /api/estado`
    *   Verifica que la API esté funcionando. Devuelve `{"estado": "ok"}`.

*   `GET /api/reformas`
    *   Devuelve la lista completa de todos los proyectos.

*   `GET /api/reforma/{id}`
    *   Devuelve un proyecto específico según su `id` único.

*   `GET /api/reformas/buscar/{termino}`
    *   Busca un `termino` en los campos de título, propósito, presentador y categoría de todos los proyectos.

### Listas de valores únicos

Estos endpoints devuelven una lista con todos los valores únicos para un campo determinado, sin repeticiones y ordenados alfabéticamente.

*   `GET /api/categorias`
*   `GET /api/presentadores`
*   `GET /api/beneficiarios`
*   `GET /api/financiamientos`

### Filtros

Estos endpoints devuelven una lista de proyectos que coinciden con un valor específico.

*   `GET /api/reformas/categoria/{valor}`
*   `GET /api/reformas/presentador/{valor}`
*   `GET /api/reformas/beneficiario/{valor}`
*   `GET /api/reformas/financiamiento/{valor}`
