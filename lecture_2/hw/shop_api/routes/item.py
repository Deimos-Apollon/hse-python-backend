import http
from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import NonNegativeInt, PositiveInt, NonNegativeFloat

from lecture_2.hw.shop_api.database.main import (items, item_id_generator)
from lecture_2.hw.shop_api.models.item import (
    Item, ItemCreate, ItemReplace, ItemModify
)

router = APIRouter(prefix="/item")


@router.post('/', status_code=HTTPStatus.CREATED)
async def create_item(item_info: ItemCreate) -> Item:
    new_item = Item(id=next(item_id_generator), name=item_info.name, price=item_info.price)
    items[new_item.id] = new_item
    return new_item


@router.get('/{id}')
async def get_item(id: int) -> Item:
    item = items.get(id, None)

    if item is None or item.deleted:
        raise HTTPException(HTTPStatus.NOT_FOUND)
    return item

@router.get('/')
async def get_item_list(
        offset: Optional[NonNegativeInt] = 0,
        limit: Optional[PositiveInt] = 10,
        min_price: Optional[NonNegativeFloat] = None,
        max_price: Optional[NonNegativeFloat] = None,
        show_deleted: bool = False
) -> list[Item]:
    filtered_items = [item for item in items.values()
        if (
            (min_price is None or item.price >= min_price) and
            (max_price is None or item.price <= max_price) and
            (show_deleted or not item.deleted)
        )
    ]
    return filtered_items[offset:offset+limit]


@router.put("/{id}")
async def replace_item(id: int, item: ItemReplace) -> Item:
    old_item = items.get(id, None)
    if item is None:
        raise HTTPException(HTTPStatus.NOT_FOUND)
    old_item.name = item.name
    old_item.price = item.price
    old_item.deleted = item.deleted
    return old_item


@router.patch("/{id}")
async def modify_item(id: int, item_info: ItemModify) -> Item:
    item = items.get(id, None)
    if item is None or item.deleted:
        raise HTTPException(status_code=http.HTTPStatus.NOT_MODIFIED)
    item.name = item.name if item_info.name else item.name
    item.price = item.price if item_info.price else item.price
    return item


@router.delete("/{id}")
async def delete_item(id: int) -> Item:
    item = items.get(id, None)
    if item is None:
        raise HTTPException(status_code=http.HTTPStatus.NOT_FOUND)
    item.deleted = True
    return item
