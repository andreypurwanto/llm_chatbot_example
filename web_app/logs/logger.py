import logging
from web_app.logs.context_filter import ContextFilter

handler = logging.StreamHandler()
formatter = logging.Formatter(
    '[%(asctime)s] [%(levelname)s] [%(trace_id)s] [%(process)s] [%(thread)s] %(filename)s:%(lineno)s : %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addFilter(ContextFilter())
logger.addHandler(handler)

LOG = logger
