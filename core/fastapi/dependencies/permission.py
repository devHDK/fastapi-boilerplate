from abc import ABC, abstractmethod
from typing import Type

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Request
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase
from starlette import status

from app.container import Container
from app.user.domain.usecase.user import UserUseCase
from core.exceptions import CustomException


class UnauthorizedException(CustomException):
    code = status.HTTP_401_UNAUTHORIZED
    error_code = "UNAUTHORIZED"
    message = ""


class BasePermission(ABC):
    exception = CustomException

    @abstractmethod
    async def has_permission(self, request: Request) -> bool:
        """has permssion"""


class IsAuthenticated(BasePermission):
    exception = UnauthorizedException

    async def has_permission(self, request: Request) -> bool:
        # 사용자가 인증되었는지 확인
        return request.user.id is not None


class IsAdmin(BasePermission):
    exception = UnauthorizedException

    @inject
    async def has_permission(
        self,
        request: Request,
        usecase: UserUseCase = Depends(Provide[Container.user_service]),
    ) -> bool:
        # 사용자가 관리자 권한을 가지고 있는지 확인
        user_id = request.user.id
        if not user_id:
            return False

        return await usecase.is_admin(user_id=user_id)


class AllowAll(BasePermission):
    async def has_permission(self, request: Request) -> bool:
        # 모든 요청을 허용
        return True


class PermissionDependency(SecurityBase):
    def __init__(self, permissions: list[Type[BasePermission]]):
        self.permissions = permissions
        self.model: APIKey = APIKey(**{"in": APIKeyIn.header}, name="Authorization")
        self.scheme_name = self.__class__.__name__

    async def __call__(self, request: Request):
        # 요청에 대해 모든 권한을 확인
        for permission in self.permissions:
            cls = permission()
            if not await cls.has_permission(request=request):
                raise cls.exception
