import json
from math_functions import factorial, fibonacci, mean
from utils import send_json

from typing import Any, Callable, Awaitable


async def get_factorial(send: Callable[[dict[str, Any]], Awaitable[None]],
                        path_components: list[str], parameters: dict[str, str], body: str):
    if 'n' not in parameters:
        await send_json(send, 422, {"error": "Can't read `n` from url"})
        return
    n = parameters['n'][0]
    try:
        n = int(n)
    except ValueError as e:    
        await send_json(send, 422, {"error": "Error reading `n` from url"})
        return 

    try:
        res = factorial(n)
        await send_json(send, 200, {"result": res})
    except ValueError as e:    
        await send_json(send, 400, {"error": repr(e)})


async def get_fibonacci(send: Callable[[dict[str, Any]], Awaitable[None]],
                        path_components: list[str], parameters: dict[str, str], body: str):
    if len(path_components) != 1:
        await send_text(send, 422, {"error": "Can't read `n` from url path"})
        return
    n = path_components[0]
    try:
        n = int(n)
    except ValueError as e:    
        await send_json(send, 422, {"error": "Error reading `n` from url"})
        return

    try:
        res = fibonacci(n)
        await send_json(send, 200, {"result": res})
    except ValueError as e:    
        await send_json(send, 400, {"error": repr(e)})


async def get_mean(send: Callable[[dict[str, Any]], Awaitable[None]],
                   path_components: list[str], parameters: dict[str, str], body: str):
    if not body:
        await send_json(send, 422, {"error": "Can't read `data` from url"})
        return
    try:
        data = json.loads(body)
        if type(data) != list or \
            any(type(x) not in (float, int) for x in data):
            raise ValueError()
    except (json.decoder.JSONDecodeError, ValueError)  as e:    
        await send_json(send, 422, {"error": "Error reading `data` from url"})
        return

    try:
        assert len(data) != 0, "List `data` is empty."
        res = mean(data)
        await send_json(send, 200, {"result": res})
    except (ValueError, AssertionError) as e:    
        await send_json(send, 400, {"error": repr(e)})