import uvicorn
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from lecture_2.hw.shop_api.routes.item import router as item_router
from lecture_2.hw.shop_api.routes.cart import router as cart_router

app = FastAPI(title="Shop API")
app.include_router(item_router)
app.include_router(cart_router)
Instrumentator().instrument(app).expose(app)
