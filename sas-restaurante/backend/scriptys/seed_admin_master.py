from app.core.database import SessionLocal
from app.modules.gestao.models.user import User
from app.core.security.password import hash_password
from app.core.roles import UserRole


def run():
    db = SessionLocal()

    try:
        exists = (
            db.query(User)
            .filter(User.role == UserRole.ADMIN_MASTER.value)
            .first()
        )

        if exists:
            print("✔ ADMIN_MASTER já existe")
            return

        admin = User(
            name="Admin Master",
            email="admin@system.local",
            password_hash=hash_password("admin123"),
            role=UserRole.ADMIN_MASTER.value,
            tenant_id=None,
            is_active=True,
        )

        db.add(admin)
        db.commit()

        print("🚀 ADMIN_MASTER criado com sucesso")
        print("📧 email: admin@system.local")
        print("🔑 senha: admin123")

    finally:
        db.close()


if __name__ == "__main__":
    run()
