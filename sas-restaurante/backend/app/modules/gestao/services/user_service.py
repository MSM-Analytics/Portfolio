from app.modules.gestao.models.user import User
from app.modules.gestao.services.base_service import BaseService, PermissionDenied


class UserNotFound(Exception):
    pass


class UserService(BaseService):

    def list_users(self, skip: int = 0, limit: int = 10):
        self.require_admin()

        query = (
            self.db.query(User)
            .filter(User.tenant_id == self.tenant_id)
        )

        total = query.count()

        items = (
            query
            .offset(skip)
            .limit(limit)
            .all()
        )

        return items, total
