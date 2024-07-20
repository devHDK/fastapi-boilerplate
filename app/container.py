from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from app.auth.application.service.jwt import JwtService
from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepo
from app.user.application.service.user import UserService


# 의존성 주입 컨테이너 클래스 정의
class Container(DeclarativeContainer):
    # 의존성 주입 설정
    wiring_config = WiringConfiguration(packages=["app"])

    # UserSQLAlchemyRepo 싱글톤 인스턴스 생성
    user_repo = Singleton(UserSQLAlchemyRepo)
    # UserRepositoryAdapter 팩토리 인스턴스 생성, user_repo 주입
    user_repo_adapter = Factory(UserRepositoryAdapter, user_repo=user_repo)
    # UserService 팩토리 인스턴스 생성, repository 주입
    user_service = Factory(UserService, repository=user_repo_adapter)

    # JwtService 팩토리 인스턴스 생성
    jwt_service = Factory(JwtService)
