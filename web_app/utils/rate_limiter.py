# from fastapi import HTTPException, status, Request
# from functools import wraps

# from app.api.dependencies.rate_limiter import RateLimiter

# rate_limiter_moving = RateLimiter(algorithm='moving_window')
# rate_limiter_fixed = RateLimiter(algorithm='fixed_window')


# def get_key_limiter(request: Request, identifier: str = 'ip') -> str:
#     if identifier == 'ip':
#         return f'rate_limit:{request.client.host}:{request.url.path}'

#     if identifier == 'user_session':
#         user_session = request.headers.get('Authorization')
#         if not user_session:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail='Authorization header is mandatory',
#             )
#         return f'rate_limit:{user_session}:{request.url.path}'

#     raise ValueError(f'identifier {identifier} is invalid')


# def rate_limit_healthcheck(request: Request) -> bool:
#     max_requests = 5
#     window = 30
#     identifier = 'ip'
#     key = get_key_limiter(request, identifier)
#     if rate_limiter_fixed.is_rate_limited(key, max_requests, window):
#         raise HTTPException(
#             status_code=status.HTTP_429_TOO_MANY_REQUESTS,
#             detail='too many requests'
#         )


# def rate_limit_search(request: Request) -> bool:
#     max_requests = 50
#     window = 30
#     identifier = 'user_session'
#     key = get_key_limiter(request, identifier)
#     if rate_limiter_fixed.is_rate_limited(key, max_requests, window):
#         raise HTTPException(
#             status_code=status.HTTP_429_TOO_MANY_REQUESTS,
#             detail='too many requests'
#         )
