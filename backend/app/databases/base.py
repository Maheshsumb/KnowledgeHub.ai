from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass



from app.models.membership import Membership
from app.models.organization import Organization
from app.models.workspace import Workspace
from app.models.document import Document