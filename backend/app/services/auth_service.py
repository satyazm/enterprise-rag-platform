from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.database.models import User, UserRole


async def seed_default_users(db: AsyncSession) -> None:
    defaults = [
        ("admin@example.com", "admin123", "Platform Admin", UserRole.ADMIN),
        ("analyst@example.com", "analyst123", "Data Analyst", UserRole.ANALYST),
        ("viewer@example.com", "viewer123", "Knowledge Viewer", UserRole.VIEWER),
    ]
    for email, password, name, role in defaults:
        existing = await db.execute(select(User).where(User.email == email))
        if existing.scalar_one_or_none():
            continue
        db.add(User(email=email, hashed_password=hash_password(password), full_name=name, role=role))
    await db.commit()
