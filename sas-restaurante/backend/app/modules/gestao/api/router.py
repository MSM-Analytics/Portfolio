from fastapi import APIRouter, Depends, HTTPException, status
import uuid

from app.deps import get_current_user

from app.core.dependencies import pagination_params
from app.core.security.role_guard import require_roles
from app.core.roles import UserRole
from app.core.security.password import hash_password

from app.modules.gestao.models.user import User
from app.modules.gestao.schemas.user import UserList
from app.modules.gestao.services.user_service import UserService, UserNotFound
from app.modules.gestao.services.base_service import PermissionDenied
from app.modules.gestao.api.category_router import router as category_router
from app.modules.gestao.api.product_router import router as product_router


router = APIRouter(
    prefix="/gestao",
    tags=["Gestão"]
)

# inclui os sub-routers corretamente
router.include_router(category_router)
router.include_router(product_router)


@router.get("/users", response_model=UserList)
def listar_usuarios(
    user: User = Depends(get_current_user),
    pagination: dict = Depends(pagination_params),
):
    service = UserService.from_user(user)

    users, total = service.list_users(
        skip=pagination["skip"],
        limit=pagination["limit"]
    )

    return {
        "items": users,
        "total": total
    }

@router.post("/tenants", status_code=201)
def create_tenant(
    payload: dict,
    user: dict = Depends(require_roles(UserRole.ADMIN_MASTER)),
):
    """
    Cria um novo tenant lógico e o ADMIN do tenant
    """

    # validação mínima
    admin_email = payload.get("email")
    admin_password = payload.get("password")
    admin_name = payload.get("name", "Admin Tenant")

    if not admin_email or not admin_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email and password are required",
        )

    # gera tenant_id lógico
    tenant_id = uuid.uuid4().hex

    service = UserService.from_user(user)

    # garante que não existe usuário com o mesmo email
    if service.exists_by_email(admin_email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    admin = User(
        name=admin_name,
        email=admin_email,
        password_hash=hash_password(admin_password),
        role=UserRole.ADMIN_TENANT.value,
        tenant_id=tenant_id,
        is_active=True,
    )

    service.db.add(admin)
    service.db.commit()

    return {
        "tenant_id": tenant_id,
        "admin_user_id": admin.id,
        "admin_email": admin.email,
    }

