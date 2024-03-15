def gen_request_id() -> str:
    global _request_id
    request_id = f'#{_request_id}'
    _request_id += 1
    return request_id


# Private


_request_id = 0
