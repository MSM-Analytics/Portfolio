from app.core.database import get_tenant_session


class PermissionDenied(Exception):
    pass


class BaseService:
    def __init__(self, db, current_user):
        self.db = db
        self.current_user = current_user
        self.tenant_id = current_user.tenant_id

    @classmethod
    def from_user(cls, current_user):
        """
        Factory padrão para criar services já
        amarrados ao tenant do usuário autenticado
        """
        db = get_tenant_session(current_user.tenant_id)
        return cls(db=db, current_user=current_user)

    def require_admin(self):
        if not self.current_user.is_admin:
            raise PermissionDenied("Acesso negado")
