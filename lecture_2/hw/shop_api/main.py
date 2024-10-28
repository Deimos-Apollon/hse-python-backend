import uvicorn
from fastapi import FastAPI

from lecture_2.hw.shop_api.routes.item import router as item_router
from lecture_2.hw.shop_api.routes.cart import router as cart_router

app = FastAPI(title="Shop API")
app.include_router(item_router)
app.include_router(cart_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")