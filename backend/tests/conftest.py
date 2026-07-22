import asyncio
import os
import pytest
from httpx import AsyncClient, ASGITransport
import psycopg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from alembic.config import Config
from alembic import command

# Setup test DB environment variables BEFORE importing app/settings
TEST_DB_NAME = "knowledgehub_test"
TEST_DATABASE_URL = f"postgresql+asyncpg://postgres:postgres@localhost:5433/{TEST_DB_NAME}"
TEST_DATABASE_URL_SYNC = f"postgresql+psycopg://postgres:postgres@localhost:5433/{TEST_DB_NAME}"

os.environ["DATABASE_URL"] = TEST_DATABASE_URL
os.environ["DATABASE_URL_SYNC"] = TEST_DATABASE_URL_SYNC

from app.main import app
from app.databases.session import get_db
from app.models.enums import OrganizationRole
from app.core.security import create_access_token
from tests.factories.user_factory import create_user
from tests.factories.organization_factory import create_organization
from tests.factories.membership_factory import create_membership

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    try:
        conn = psycopg.connect(
            "postgresql://postgres:postgres@localhost:5433/postgres",
            autocommit=True
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{TEST_DB_NAME}'")
        cursor.execute(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}")
        cursor.execute(f"CREATE DATABASE {TEST_DB_NAME}")
        conn.close()
    except Exception as e:
        pytest.fail(f"Could not create test database: {e}")

    # Run Alembic migrations
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL_SYNC)
    command.upgrade(alembic_cfg, "head")

    yield

    try:
        conn = psycopg.connect(
            "postgresql://postgres:postgres@localhost:5433/postgres",
            autocommit=True
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{TEST_DB_NAME}'")
        cursor.execute(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}")
        conn.close()
    except Exception as e:
        pass

engine = create_async_engine(TEST_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

@pytest.fixture
async def db_session():
    # Use nested transactions to rollback after each test
    async with engine.connect() as connection:
        transaction = await connection.begin()
        async with TestingSessionLocal(bind=connection) as session:
            yield session
            await session.rollback()
        await transaction.rollback()

@pytest.fixture
async def client(db_session: AsyncSession):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()

@pytest.fixture
async def test_user(db_session: AsyncSession):
    user, raw_password = await create_user(db_session)
    return user, raw_password

@pytest.fixture
async def owner_user(db_session: AsyncSession):
    user, raw_password = await create_user(db_session)
    return user, raw_password

@pytest.fixture
async def admin_user(db_session: AsyncSession):
    user, raw_password = await create_user(db_session)
    return user, raw_password

@pytest.fixture
async def member_user(db_session: AsyncSession):
    user, raw_password = await create_user(db_session)
    return user, raw_password

@pytest.fixture
async def viewer_user(db_session: AsyncSession):
    user, raw_password = await create_user(db_session)
    return user, raw_password

@pytest.fixture
async def organization(db_session: AsyncSession, owner_user, admin_user, member_user, viewer_user):
    owner, _ = owner_user
    org = await create_organization(db_session, owner_id=owner.id)
    
    await create_membership(db_session, owner.id, org.id, OrganizationRole.OWNER)
    
    admin, _ = admin_user
    await create_membership(db_session, admin.id, org.id, OrganizationRole.ADMIN)
    
    member, _ = member_user
    await create_membership(db_session, member.id, org.id, OrganizationRole.MEMBER)
    
    viewer, _ = viewer_user
    await create_membership(db_session, viewer.id, org.id, OrganizationRole.VIEWER)
    
    return org

@pytest.fixture
def test_token(test_user):
    user, _ = test_user
    return create_access_token(str(user.id))

@pytest.fixture
def owner_token(owner_user):
    user, _ = owner_user
    return create_access_token(str(user.id))

@pytest.fixture
def admin_token(admin_user):
    user, _ = admin_user
    return create_access_token(str(user.id))

@pytest.fixture
def member_token(member_user):
    user, _ = member_user
    return create_access_token(str(user.id))

@pytest.fixture
def viewer_token(viewer_user):
    user, _ = viewer_user
    return create_access_token(str(user.id))
