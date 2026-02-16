from enum import Enum


class SaleStatus(str, Enum):
    OPEN = "OPEN"                 # venda criada, sem pagamento
    PARTIALLY_PAID = "PARTIALLY_PAID"  # pagamento parcial
    PAID = "PAID"                 # totalmente paga
    CANCELED = "CANCELED"         # cancelada
