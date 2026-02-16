from enum import Enum

class CashflowCategory(str, Enum):
    SALE = "SALE"
    REFUND = "REFUND"
    EXPENSE = "EXPENSE"
