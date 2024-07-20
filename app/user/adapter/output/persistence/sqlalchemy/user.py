from sqlalchemy import and_, or_, select

from app.user.domain.entity.user import User
from app.user.domain.repository.user import UserRepo
from core.db.session import session, session_factory


class UserSQLAlchemyRepo(UserRepo):
    async def get_users(
        self,
        *,
        limit: int = 12,
        prev: int | None = None,
    ) -> list[User]:
        query = select(User)  # User 테이블에서 모든 사용자 선택

        if prev:
            query = query.where(User.id < prev)  # 이전 사용자 ID보다 작은 사용자 선택

        if limit > 12:
            limit = 12  # 최대 제한을 12로 설정

        query = query.limit(limit)  # 선택할 사용자 수 제한
        async with session_factory() as read_session:
            result = await read_session.execute(query)  # 쿼리 실행

        return result.scalars().all()  # 결과 반환

    async def get_user_by_email_or_nickname(
        self,
        *,
        email: str,
        nickname: str,
    ) -> User | None:
        async with session_factory() as read_session:
            stmt = await read_session.execute(
                select(User).where(or_(User.email == email, User.nickname == nickname)),
            )  # 이메일 또는 닉네임으로 사용자 선택
            return stmt.scalars().first()  # 첫 번째 결과 반환

    async def get_user_by_id(self, *, user_id: int) -> User | None:
        async with session_factory() as read_session:
            stmt = await read_session.execute(
                select(User).where(User.id == user_id)
            )  # ID로 사용자 선택
            return stmt.scalars().first()  # 첫 번째 결과 반환

    async def get_user_by_email_and_password(
        self,
        *,
        email: str,
        password: str,
    ) -> User | None:
        async with session_factory() as read_session:
            stmt = await read_session.execute(
                select(User).where(and_(User.email == email, password == password))
            )  # 이메일과 비밀번호로 사용자 선택
            return stmt.scalars().first()  # 첫 번째 결과 반환

    async def save(self, *, user: User) -> None:
        session.add(user)  # 사용자 저장
