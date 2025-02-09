# from fastapi import HTTPException, status
# from datetime import timedelta
# import time
# import redis
# from app.stack.cache import cache_con


# class RateLimiter:
#     def __init__(self, algorithm: str = 'fixed_window') -> None:
#         self.redis_conn = cache_con
#         self.algorithm = algorithm

#     def is_rate_limited(self, key: str, max_requests: int, window: int) -> bool:
#         if self.algorithm == 'moving_window':
#             return self.__moving_window(key, max_requests, window)

#         if self.algorithm == 'fixed_window':
#             return self.__fixed_window(key, max_requests, window)

#         raise NotImplementedError(
#             f'algorithm {self.algorithm} not implemented')

#     def __moving_window(self, key: str, max_requests: int, window: int) -> bool:
#         """moving window algorithm, step:
#         1. remove counter that add before `window_start` (zremrangebyscore)
#             window_start = now - window
#         2. get counter between `window_start` and `now`
#         3. add 1 counter
#         4. return False if counter > max_requests

#         Args:
#             key (str): key in cache, default is client-ip-address + path-endpoint
#             max_requests (int): number of maximum request in certain window time
#             window (int): time in seconds

#         Raises:
#             HTTPException: raise error if redis got error

#         Returns:
#             bool: False if counter > max_requests else True
#         """
#         current = int(time.time())
#         window_start = current - window
#         with self.redis_conn.pipeline() as pipe:
#             try:
#                 pipe.zremrangebyscore(key, 0, window_start)
#                 pipe.zcard(key)
#                 pipe.zadd(key, {current: current})
#                 pipe.expire(key, window)
#                 results = pipe.execute()
#             except redis.RedisError as e:
#                 raise HTTPException(
#                     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                     detail=f'Redis error: {str(e)}'
#                 )
#         return results[1] > max_requests

#     def __fixed_window(self, key: str, max_requests: int, window: int) -> bool:
#         """fixed window algorithm, step:
#         1. check if key exist or not
#         2. if exist, create counter with TTL = window else add increment by 1
#         3. return False if counter > max_requests

#         Args:
#             key (str): key in cache, default is client-ip-address + path-endpoint
#             max_requests (int): number of maximum request in certain window time
#             window (int): time in seconds

#         Raises:
#             HTTPException: raise error if redis got error

#         Returns:
#             bool: False if counter > max_requests else True
#         """
#         if self.redis_conn.exists(key):
#             counter = self.redis_conn.incr(key)
#         else:
#             with self.redis_conn.pipeline() as pipe:
#                 pipe.incr(key)
#                 pipe.expire(key, timedelta(seconds=window))
#                 results = pipe.execute()

#                 # index 0 is operation for 0-th in pipeline
#                 counter = results[0]

#         return counter > max_requests
