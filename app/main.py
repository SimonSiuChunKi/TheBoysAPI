from fastapi import FastAPI
from app.api.api_v1.api import router as api_router
from mangum import Mangum
from fastapi.responses import RedirectResponse



app = FastAPI(openapi_prefix='/prod/')


@app.get("/health")
async def health():
  return "OK"

@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

app.include_router(api_router, prefix="/api/v1")

handler = Mangum(app)

