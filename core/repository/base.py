from typing import TypeVar, Type, Generic

from sqlalchemy import select, update, delete

from core.db.session import Base, session
from core.repository.enum import SynchronizeSessionEnum

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepo(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_by_id(self, id: int) -> ModelType | None:
        # 주어진 ID로 모델을 조회하는 메서드
        query = select(self.model).where(self.model.id == id)
        return await session.execute(query).scalars().first()

    async def update_by_id(
        self,
        id: int,
        params: dict,
        synchronize_session: SynchronizeSessionEnum = False,
    ) -> None:
        # 주어진 ID로 모델을 업데이트하는 메서드
        query = (
            update(self.model)
            .where(self.model.id == id)
            .values(**params)
            .execution_options(synchronize_session=synchronize_session)
        )
        await session.execute(query)

    async def delete(self, model: ModelType) -> None:
        # 주어진 모델을 삭제하는 메서드
        await session.delete(model)

    async def delete_by_id(
        self,
        id: int,
        synchronize_session: SynchronizeSessionEnum = False,
    ) -> None:
        # 주어진 ID로 모델을 삭제하는 메서드
        query = (
            delete(self.model)
            .where(self.model.id == id)
            .execution_options(synchronize_session=synchronize_session)
        )
        await session.execute(query)

    async def save(self, model: ModelType) -> ModelType:
        # 주어진 모델을 저장하는 메서드
        saved = await session.add(model)
        return saved
