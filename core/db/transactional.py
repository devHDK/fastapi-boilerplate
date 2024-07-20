from functools import wraps

from core.db import session


class Transactional:
    def __call__(self, func):
        @wraps(func)
        async def _transactional(*args, **kwargs):
            try:
                # 함수 실행
                result = await func(*args, **kwargs)
                # 성공 시 커밋
                await session.commit()
            except Exception as e:
                # 예외 발생 시 롤백
                await session.rollback()
                raise e

            return result

        return _transactional
