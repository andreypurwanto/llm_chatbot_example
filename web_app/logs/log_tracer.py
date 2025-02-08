from typing import Union
from uuid import uuid4

from web_app.logs.current_thread import CurrentThread


def set_get_trace_id(trace_id: Union[str, None] = None) -> None:
    current_thread = CurrentThread()
    if not trace_id:
        trace_id = str(uuid4())
    current_thread.set('trace_id', trace_id)
    return trace_id
