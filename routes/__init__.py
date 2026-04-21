"""Routers FastAPI extrets de server.py.

Cada submòdul exporta un `router` (`fastapi.APIRouter`) que server.py
registra via `app.include_router(router)`. Aixo ens permet dividir els
~75 endpoints del monolit sense canviar la URL ni el contracte de cap.
"""
