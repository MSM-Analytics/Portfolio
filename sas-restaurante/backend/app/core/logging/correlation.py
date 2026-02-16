import uuid
from contextvars import ContextVar

correlation_id_ctx = ContextVar("correlation_id", default=None)

def get_correlation_id():
    return correlation_id_ctx.get()

def set_correlation_id(value: str):
    correlation_id_ctx.set(value or str(uuid.uuid4()))
