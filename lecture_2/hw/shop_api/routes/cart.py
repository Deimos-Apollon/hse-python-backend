from http import HTTPStatus
from statistics import quantiles
from typing import Optional

from fastapi import APIRouter, HTTPException, Response
from pydantic import NonNegativeInt, PositiveInt, NonNegativeFloat

from lecture_2.hw.shop_api.database.main import (carts, items, cart_id_generator, item_id_generator)
from lecture_2.hw.shop_api.models.cart import (
    Cart, ItemInCart
)
from lecture_2.hw.shop_api.routes.item import get_item

router = APIRouter(prefix="/cart")

# works as RPC
@router.post('/', status_code=HTTPStatus.CREATED)
async def create_cart(response: Response) -> dict:
    new_cart = Cart(id=next(cart_id_generator))
    carts[new_cart.id] = new_cart
    response.headers['location'] = f'/cart/{new_cart.id}'
    return {"id": new_cart.id}


@router.get('/{id}')
async def get_cart(id: int) -> Cart:
    cart = carts.get(id, None)
    if cart is None:
        raise HTTPException(HTTPStatus.NOT_FOUND)
    update_cart_items(cart.id)
    return cart


@router.get('/')
async def get_cart_list(
        offset: Optional[NonNegativeInt] = 0,
        limit: Optional[PositiveInt] = 10,
        min_price: Optional[NonNegativeFloat] = None,
        max_price: Optional[NonNegativeFloat] = None,
        min_quantity: Optional[NonNegativeInt] = None,
        max_quantity: Optional[NonNegativeInt] = None
) -> list[Cart]:
    update_all_carts_items()
    filtered_carts = [cart for cart in carts.values()
        if (
            (min_price is None or cart.price >= min_price) and
            (max_price is None or cart.price <= max_price) and
            (min_quantity is None or count_total_quantity(cart.id) >= min_quantity) and
            (max_quantity is None or count_total_quantity(cart.id) <= max_quantity)
        )
    ]
    return filtered_carts[offset:offset+limit]

@router.post('/{cart_id}/add/{item_id}', status_code=HTTPStatus.CREATED)
async def add_item_to_cart(cart_id: int, item_id: int) -> ItemInCart:
    cart = carts.get(cart_id, None)
    if cart is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Cart not found")
    item = items.get(item_id, None)
    if item is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Item not found")

    if item.deleted:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Item deleted")

    for cart_item in cart.items:
        if cart_item.id == item_id:
            cart_item.quantity += 1
            break
    else:
        new_item = ItemInCart(id=item.id, name=item.name)
        cart.items.append(new_item)
        cart_item = new_item
    cart.price += item.price
    return cart_item


def update_cart_items(cart_id):
    """Обновляем для всех если card_id=None, иначе для корзины с id `cart_id"""
    cart = carts[cart_id]
    for cart_item in cart.items:
        item = items[cart_item.id]
        if item.deleted:
            cart_item.available = False
            cart.price -= item.price * cart_item.quantity

def update_all_carts_items():
    for id in carts:
        update_cart_items(id)

def count_total_quantity(cart_id):
    cart = carts[cart_id]
    update_cart_items(cart_id)
    quantity = 0
    for cart_item in cart.items:
        if cart_item.available:
            quantity += cart_item.quantity
    return quantity
