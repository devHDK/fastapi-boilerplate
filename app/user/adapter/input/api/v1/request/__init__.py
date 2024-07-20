from pydantic import BaseModel, Field


# 로그인 요청 모델 정의
class LoginRequest(BaseModel):
    email: str = Field(..., description="Email")  # 이메일 필드
    password: str = Field(..., description="Password")  # 비밀번호 필드


# 사용자 생성 요청 모델 정의
class CreateUserRequest(BaseModel):
    email: str = Field(..., description="Email")  # 이메일 필드
    password1: str = Field(..., description="Password1")  # 비밀번호1 필드
    password2: str = Field(..., description="Password2")  # 비밀번호2 필드
    nickname: str = Field(..., description="Nickname")  # 닉네임 필드
    lat: float = Field(..., description="Lat")  # 위도 필드
    lng: float = Field(..., description="Lng")  # 경도 필드
