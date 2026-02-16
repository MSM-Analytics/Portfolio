from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.settings import settings
from app.core.database import Base, engine
from app.core.middleware.audit_middleware import AuditMiddleware
from app.core.logging.middleware import LoggingMiddleware

# =========================
# IMPORTAR MODELS (ANTES DAS TABELAS)
# =========================
from app.modules.gestao.models import *

# =========================
# IMPORTAR ROUTERS
# =========================
from app.modules.gestao.api.auth_router import router as auth_router
from app.modules.gestao.api.router import router as gestao_router
from app.modules.gestao.api.product_router import router as product_router
from app.modules.gestao.api.category_router import router as category_router
from app.modules.gestao.api.payment_method_router import router as payment_method_router
from app.modules.gestao.api.sale_router import router as sale_router
from app.modules.gestao.api.refund_router import router as refund_router
from app.modules.gestao.api.cash_closure_router import router as cash_closure_router
from app.modules.gestao.api.financial_report_router import router as financial_report_router
from app.modules.gestao.api.report_router import router as report_router
from app.modules.gestao.api.export_router import router as export_router
from app.modules.gestao.api.dashboard_router import router as dashboard_router
from app.modules.gestao.api.charts_router import router as charts_router
from app.modules.gestao.api.alerts_router import router as alerts_router
from app.modules.gestao.api.goals_router import router as goals_router
from app.modules.gestao.api.forecast_router import router as forecast_router
from app.modules.gestao.api.audit_router import router as audit_router

# =========================
# APP
# =========================
app = FastAPI()

# print("🔥 FASTAPI SUBIU COM CORS")

# =========================
# CORS (OBRIGATÓRIO PARA ANGULAR)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",  # Angular
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# MIDDLEWARES (DEPOIS DO CORS)
# =========================
app.add_middleware(AuditMiddleware)
app.add_middleware(LoggingMiddleware)

# =========================
# HEALTH CHECK
# =========================
@app.get("/", tags=["health"])
def root_health_check():
    return {
        "status": "ok",
        "service": settings.app_name,
        "env": settings.env,
    }

@app.get("/health", tags=["health"])
def api_health():
    return {"status": "ok"}

# =========================
# CRIAR TABELAS
# =========================
Base.metadata.create_all(bind=engine)

# =========================
# REGISTRAR ROUTERS
# =========================
app.include_router(auth_router)

app.include_router(gestao_router)

app.include_router(product_router, prefix="/gestao")
app.include_router(category_router, prefix="/gestao")
app.include_router(payment_method_router, prefix="/gestao")
app.include_router(sale_router, prefix="/gestao")
app.include_router(refund_router, prefix="/gestao")
app.include_router(cash_closure_router, prefix="/gestao")
app.include_router(financial_report_router, prefix="/gestao")
app.include_router(report_router, prefix="/gestao")
app.include_router(export_router, prefix="/gestao")
app.include_router(dashboard_router, prefix="/gestao")
app.include_router(charts_router, prefix="/gestao")
app.include_router(alerts_router, prefix="/gestao")
app.include_router(goals_router, prefix="/gestao")
app.include_router(forecast_router, prefix="/gestao")
app.include_router(audit_router, prefix="/gestao")


"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.modules.gestao.models import *  # força registry completo
from app.core.dependencies import get_db
from app.core.security.jwt import create_access_token

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/auth/login")
async def test_login(db: Session = Depends(get_db)):

    # 🔹 BUSCA USUÁRIO REAL
    user = db.query(User).filter(User.email == "admin@teste.com").first()

    if not user:
        return {"error": "Usuário não encontrado"}

    # 🔐 JWT COM ROLE REAL
    access_token = create_access_token(
        user_id=user.id,
        role=user.role,          # 👈 AUTOMÁTICO
        tenant_id=user.tenant_id
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "tenant_id": user.tenant_id
        }
    }

"""

