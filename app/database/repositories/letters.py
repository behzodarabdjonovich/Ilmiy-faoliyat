from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import Letter, LetterVersion, User

async def create_letter(s: AsyncSession, **data) -> Letter:
    obj = Letter(**data)
    s.add(obj)
    await s.flush()
    s.add(LetterVersion(letter_id=obj.id, version_number=1, content=obj.content))
    await s.commit()
    await s.refresh(obj)
    return obj

async def add_version(s: AsyncSession, letter: Letter, content: str, instruction: str | None = None):
    n = (await s.execute(
        select(func.coalesce(func.max(LetterVersion.version_number), 0)).where(LetterVersion.letter_id == letter.id)
    )).scalar_one() + 1
    s.add(LetterVersion(letter_id=letter.id, version_number=n, content=content, edit_instruction=instruction))
    letter.content = content
    await s.commit()

async def list_user_letters(s: AsyncSession, user_id: int, offset: int = 0, limit: int = 10):
    q = select(Letter).where(Letter.user_id == user_id).order_by(Letter.created_at.desc()).offset(offset).limit(limit)
    return list((await s.execute(q)).scalars())

async def get_owned_letter(s: AsyncSession, letter_id: int, telegram_id: int) -> Letter | None:
    q = (select(Letter).join(User, User.id == Letter.user_id)
         .where(Letter.id == letter_id, User.telegram_id == telegram_id))
    return (await s.execute(q)).scalar_one_or_none()
