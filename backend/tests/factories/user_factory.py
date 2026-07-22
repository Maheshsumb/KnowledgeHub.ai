import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

password_hash = PasswordHash((Argon2Hasher(),))

async def create_user(
    db: AsyncSession,
    email: str = None,
    password: str = "TestPassword123!",
    full_name: str = "Test User",
    is_active: bool = True,
):
    if email is None:
        email = f"user_{uuid.uuid4().hex[:8]}@example.com"
        
    user = User(
        email=email,
        full_name=full_name,
        password_hash=password_hash.hash(password),
        is_active=is_active,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    # Return user and raw password for login tests
    return user, password
