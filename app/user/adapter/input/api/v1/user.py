from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

from app.container import Container
from app.user.adapter.input.api.v1.request import CreateUserRequest, LoginRequest
from app.user.adapter.input.api.v1.response import LoginResponse
from app.user.application.dto import CreateUserResponseDTO, GetUserListResponseDTO
from app.user.domain.command import CreateUserCommand
from app.user.domain.usecase.user import UserUseCase
from core.fastapi.dependencies import IsAdmin, PermissionDependency, IsAuthenticated

# 사용자 라우터 생성
user_router = APIRouter()


# 사용자 목록 조회 엔드포인트 정의
@user_router.get(
    "",
    response_model=list[GetUserListResponseDTO],
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))],
)
@inject
async def get_user_list(
    limit: int = Query(10, description="Limit"),  # 조회할 사용자 수 제한
    prev: int = Query(None, description="Prev ID"),  # 이전 사용자 ID
    usecase: UserUseCase = Depends(Provide[Container.user_service]),  # UserUseCase 주입
):
    return await usecase.get_user_list(limit=limit, prev=prev)  # 사용자 목록 조회


# 사용자 생성 엔드포인트 정의
@user_router.post(
    "",
    response_model=CreateUserResponseDTO,
)
@inject
async def create_user(
    request: CreateUserRequest,  # 사용자 생성 요청 데이터
    usecase: UserUseCase = Depends(Provide[Container.user_service]),  # UserUseCase 주입
):
    command = CreateUserCommand(**request.model_dump())  # CreateUserCommand 생성
    await usecase.create_user(command=command)  # 사용자 생성
    return {"email": request.email, "nickname": request.nickname}  # 응답 데이터 반환


# 사용자 로그인 엔드포인트 정의
@user_router.post(
    "/login",
    response_model=LoginResponse,
)
@inject
async def login(
    request: LoginRequest,  # 로그인 요청 데이터
    usecase: UserUseCase = Depends(Provide[Container.user_service]),  # UserUseCase 주입
):
    token = await usecase.login(
        email=request.email, password=request.password
    )  # 로그인 처리
    return {
        "token": token.token,
        "refresh_token": token.refresh_token,
    }  # 토큰 응답 데이터 반환
