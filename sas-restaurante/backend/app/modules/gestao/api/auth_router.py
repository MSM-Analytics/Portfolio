from fastapi import APIRouter, HTTPException
from app.core.database import get_tenant_session
from app.core.security.jwt import create_access_token
from app.core.security.password import verify_password
from app.modules.gestao.models.user import User
from app.modules.gestao.schemas.auth import LoginRequest
from app.core.roles import get_permissions_by_role

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(data: LoginRequest):
    db = get_tenant_session(None)

    try:
        print("➡️ LOGIN REQUEST =>", data)
        print("EMAIL BUSCADO:", data.email)
        
        user = (
            db.query(User)
            .filter(
                User.email == data.email,
                User.is_active.is_(True)
            )
            .first()
        )

        print("🧠 USER FOUND =>", user)

        if not user:
            print("❌ USER NOT FOUND:", data.email)
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

        if not verify_password(data.password, user.password_hash):
            print("❌ INVALID PASSWORD FOR:", data.email)
            raise HTTPException(status_code=401, detail="Senha inválida")

        token = create_access_token(
            user_id=user.id,
            role=user.role,
            tenant_id=user.tenant_id,
        )

        print("🔐 TOKEN GENERATED")

        permissions = get_permissions_by_role(user.role)

        print("🛡 PERMISSIONS =>", permissions)

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": str(user.id),
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "tenant_id": user.tenant_id,
                "permissions": permissions,
            }
        }
    finally:
        db.close()
        print("🔒 DB SESSION CLOSED")


