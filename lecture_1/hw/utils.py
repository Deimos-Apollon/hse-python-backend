import json


async def read_body(receive):
    """
    Read and return the entire body from an incoming ASGI message.
    """
    body = b''
    more_body = True

    while more_body:
        message = await receive()
        body += message.get('body', b'')
        more_body = message.get('more_body', False)

    return body


async def send_json(send, status_code: int, data: dict) -> None:
    await send({
        'type': 'http.response.start',
        'status': status_code,
        'headers': [
            [b'content-type', b'application/json'],
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': json.dumps(data).encode('utf8')
    })

