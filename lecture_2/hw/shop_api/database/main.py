from typing import Iterable, Tuple


def int_id_generator() -> Iterable[int]:
    i = 0
    while True:
        yield i
        i += 1

def init_db() -> Tuple[dict, dict, callable, callable]:
    carts = {}
    items = {}

    cart_id_generator = int_id_generator()
    item_id_generator = int_id_generator()
    
    return carts, items, cart_id_generator, item_id_generator 

carts, items, cart_id_generator, item_id_generator = init_db()
