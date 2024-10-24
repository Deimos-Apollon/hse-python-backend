from handlers import get_factorial, get_fibonacci, get_mean
from utils import read_body, send_json

from typing import Any, Callable, Awaitable
from urllib.parse import parse_qs


async def app(scope: dict[str, Any], 
              receive: Callable[[], Awaitable[dict[str, Any]]], 
              send: Callable[[dict[str, Any]], Awaitable[None]]) -> None:
    assert scope['type'] == 'http'

    if scope['method'] == 'GET':
        path_components = scope["path"][1:].split('/')
        parameters = parse_qs(scope["query_string"].decode())
        body = await read_body(receive)
        body = body.decode()
        first_component_processors = {'factorial': get_factorial,
                                      'fibonacci': get_fibonacci,
                                      'mean': get_mean}
        if not path_components or path_components[0] not in first_component_processors:
            await send_json(send, 404, {"error": "Requested path not found"})
        else:
            processor = first_component_processors[path_components[0]]
            await processor(send, path_components[1:], parameters, body)
    else:
        await send_json(send, 404, {"error": "Only GET is allowed"})
