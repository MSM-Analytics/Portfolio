from sqlalchemy import Column, String


class TenantMixin:

    tenant_id = Column(
        String,
        nullable=False,
        index=True,
        comment="Tenant isolator (multi-tenant contract)",
    )
