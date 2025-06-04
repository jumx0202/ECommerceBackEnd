from sqlalchemy.orm import Session
from app import schemas
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User

def init_db(db: Session) -> None:
    # 创建初始管理员用户
    user = db.query(User).filter(User.username == settings.FIRST_SUPERUSER).first()
    if not user:
        user_in = schemas.UserCreate(
            username=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            full_name="System Administrator",
            role="admin"
        )
        user = User(
            username=user_in.username,
            password_hash=get_password_hash(user_in.password),
            full_name=user_in.full_name,
            role=user_in.role
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Created superuser: {user.username}")
    else:
        print(f"Superuser {user.username} already exists") 