import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base, User, Session, Emotion, Tag
from config import DATABASE_URL

db_engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)

async def seed():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            # Criar usuário
            user = User(name="Test User")
            session.add(user)
            await session.flush()

            # Criar sessão
            mind_session = Session(user_id=user.id)
            session.add(mind_session)
            await session.flush()

            # Emoções
            emotions = [
                Emotion(session_id=mind_session.id, label="alegria", intensity=75),
                Emotion(session_id=mind_session.id, label="medo", intensity=40)
            ]
            session.add_all(emotions)

            # Tags
            tags = [Tag(name="foco"), Tag(name="ansiedade")]
            session.add_all(tags)
            await session.flush()

            # Relacionar tags à sessão
            mind_session.tags.extend(tags)

        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed())
