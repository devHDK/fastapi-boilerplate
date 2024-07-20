from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


# TimestampMixin 클래스 정의
class TimestampMixin:
    # 생성 시각을 나타내는 컬럼 정의
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),  # 기본값으로 현재 시각 설정
        nullable=False,  # null 값을 허용하지 않음
    )
    # 수정 시각을 나타내는 컬럼 정의
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),  # 기본값으로 현재 시각 설정
        onupdate=func.now(),  # 업데이트 시 현재 시각으로 갱신
        nullable=False,  # null 값을 허용하지 않음
    )
