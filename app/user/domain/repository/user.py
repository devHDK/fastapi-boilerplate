from abc import ABC, abstractmethod
from app.user.domain.entity.user import User


class UserRepo(ABC):
    @abstractmethod
    async def get_users(
        self,
        *,
        limit: int = 12,
        prev: int | None = None,
    ) -> list[User]:
        """사용자 목록 가져오기"""

    @abstractmethod
    async def get_user_by_email_or_nickname(
        self,
        *,
        email: str,
        nickname: str,
    ) -> User | None:
        """이메일 또는 닉네임으로 사용자 가져오기"""

    @abstractmethod
    async def get_user_by_id(self, *, user_id: int) -> User | None:
        """ID로 사용자 가져오기"""

    @abstractmethod
    async def get_user_by_email_and_password(
        self,
        *,
        email: str,
        password: str,
    ) -> User | None:
        """이메일과 비밀번호로 사용자 가져오기"""

    @abstractmethod
    async def save(self, *, user: User) -> None:
        """사용자 저장"""
