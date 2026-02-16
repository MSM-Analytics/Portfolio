from enum import Enum


class SaleStatus(str, Enum):
    OPEN = "OPEN"
    PAID = "PAID"
    CANCELED = "CANCELED"


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    REFUNDED = "REFUNDED"


class StockMovementType(str, Enum):
    IN = "IN"
    OUT = "OUT"
    ADJUST = "ADJUST"


class CashflowType(str, Enum):
    IN = "IN"
    OUT = "OUT"
