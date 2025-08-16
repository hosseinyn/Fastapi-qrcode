from fastapi import *
from fastapi.openapi.utils import get_openapi
from routes.qrcodes import router as qrcodes_router

app = FastAPI()

# Config open api :
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="QR Code API",
        version="0.0.1",
        summary="A qrcode generator && reader in python fastapi",
        description="This app uses fastapi backend and qrcode python library for generate and read qrcodes in a restful api",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# API Router : 
app.include_router(qrcodes_router)
