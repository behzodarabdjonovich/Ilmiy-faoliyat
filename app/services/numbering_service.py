from datetime import datetime, timezone
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import LetterCounter, Organization

async def next_number(s: AsyncSession, organization_id: int) -> str:
    # PostgreSQL transaction-scoped advisory lock serializes first-counter creation too.
    async with s.begin():
        org = await s.get(Organization, organization_id)
        if not org:
            raise ValueError("Organization not found")
        year = datetime.now(timezone.utc).year if org.reset_yearly else 0
        lock_key = organization_id * 10000 + year
        await s.execute(text("SELECT pg_advisory_xact_lock(:key)"), {"key": lock_key})
        q = (select(LetterCounter)
             .where(LetterCounter.organization_id == organization_id, LetterCounter.year == year)
             .with_for_update())
        counter = (await s.execute(q)).scalar_one_or_none()
        if counter is None:
            counter = LetterCounter(organization_id=organization_id, year=year, value=0)
            s.add(counter)
            await s.flush()
        counter.value += 1
        value = counter.value
    return f"{org.number_prefix}/{value:03d}"
