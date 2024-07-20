from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.application.dto import LoginResponseDTO
from app.user.application.exception import (
    DuplicateEmailOrNicknameException,
    PasswordDoesNotMatchException,
    UserNotFoundException,
)
from app.user.domain.command import CreateUserCommand
from app.user.domain.entity.user import User, UserRead
from app.user.domain.usecase.user import UserUseCase
from app.user.domain.vo.location import Location
from core.db import Transactional
from core.helpers.token import TokenHelper


class UserService(UserUseCase):
    def __init__(self, *, repository: UserRepositoryAdapter):
        self.repository = repository

    # 사용자 목록 조회
    async def get_user_list(
        self,
        *,
        limit: int = 12,
        prev: int | None = None,
    ) -> list[UserRead]:
        return await self.repository.get_users(limit=limit, prev=prev)

    # 사용자 생성
    @Transactional()
    async def create_user(self, *, command: CreateUserCommand) -> None:
        # 비밀번호 일치 여부 확인
        if command.password1 != command.password2:
            raise PasswordDoesNotMatchException

        # 이메일 또는 닉네임 중복 여부 확인
        is_exist = await self.repository.get_user_by_email_or_nickname(
            email=command.email,
            nickname=command.nickname,
        )
        if is_exist:
            raise DuplicateEmailOrNicknameException

        # 사용자 생성
        user = User.create(
            email=command.email,
            password=command.password1,
            nickname=command.nickname,
            location=Location(lat=command.lat, lng=command.lng),
        )
        await self.repository.save(user=user)

    # 관리자 여부 확인
    async def is_admin(self, *, user_id: int) -> bool:
        user = await self.repository.get_user_by_id(user_id=user_id)
        if not user:
            return False

        if user.is_admin is False:
            return False

        return True

    # 사용자 로그인
    async def login(self, *, email: str, password: str) -> LoginResponseDTO:
        user = await self.repository.get_user_by_email_and_password(
            email=email,
            password=password,
        )
        if not user:
            raise UserNotFoundException

        response = LoginResponseDTO(
            token=TokenHelper.encode(payload={"user_id": user.id}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"}),
        )
        return response
