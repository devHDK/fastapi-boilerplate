from contextlib import asynccontextmanager
from contextvars import ContextVar, Token
from enum import Enum
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.sql.expression import Delete, Insert, Update

from core.config import config

# 세션 컨텍스트를 저장하기 위한 ContextVar 객체
session_context: ContextVar[str] = ContextVar("session_context")


# 현재 세션 컨텍스트를 반환하는 함수
def get_session_context() -> str:
    return session_context.get()


# 세션 컨텍스트를 설정하는 함수
def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


# 세션 컨텍스트를 리셋하는 함수
def reset_session_context(context: Token) -> None:
    session_context.reset(context)


# 데이터베이스 엔진 타입을 정의하는 Enum 클래스
class EngineType(Enum):
    WRITER = "writer"
    READER = "reader"


# 데이터베이스 엔진을 생성하는 딕셔너리
engines = {
    EngineType.WRITER: create_async_engine(config.WRITER_DB_URL, pool_recycle=3600),
    EngineType.READER: create_async_engine(config.READER_DB_URL, pool_recycle=3600),
}


# 라우팅 세션 클래스 정의
class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kw):
        if self._flushing or isinstance(clause, (Update, Delete, Insert)):
            return engines[EngineType.WRITER].sync_engine
        else:
            return engines[EngineType.READER].sync_engine


# 비동기 세션 팩토리 생성
_async_session_factory = async_sessionmaker(
    class_=AsyncSession,
    sync_session_class=RoutingSession,
    expire_on_commit=False,
)

# 비동기 스코프 세션 생성
session = async_scoped_session(
    session_factory=_async_session_factory,
    scopefunc=get_session_context,
)


# 기본 베이스 클래스 정의
class Base(DeclarativeBase): ...


# 비동기 컨텍스트 매니저를 사용하여 세션을 생성하는 함수
@asynccontextmanager
async def session_factory() -> AsyncGenerator[AsyncSession, None]:
    _session = async_sessionmaker(
        class_=AsyncSession,
        sync_session_class=RoutingSession,
        expire_on_commit=False,
    )()
    try:
        yield _session
    finally:
        await _session.close()
