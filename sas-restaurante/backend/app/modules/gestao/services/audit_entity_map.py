from app.modules.gestao.models.product import Product
from app.modules.gestao.models.category import Category
from app.modules.gestao.models.sale import Sale
from app.modules.gestao.models.cash_closure import CashClosure

ENTITY_MAP = {
    "/gestao/products": Product,
    "/gestao/categories": Category,
    "/gestao/sales": Sale,
    "/cash-closure": CashClosure,
}
