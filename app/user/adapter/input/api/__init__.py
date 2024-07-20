from fastapi import APIRouter  # FastAPI의 APIRouter 임포트

from app.user.adapter.input.api.v1.user import (
    user_router as user_v1_router,
)  # v1 사용자 라우터 임포트 및 별칭 설정

router = APIRouter()  # APIRouter 인스턴스 생성
router.include_router(
    user_v1_router, prefix="/api/v1/user", tags=["User"]
)  # v1 사용자 라우터를 포함, 경로와 태그 설정

__all__ = ["router"]  # 모듈에서 내보낼 객체 정의
