from sqlalchemy import create_engine, Table, Column, Integer, Boolean, MetaData
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

engine = create_engine("sqlite+pysqlite:///gambler.db", echo=True)
Session = sessionmaker(bind=engine)
metadata = MetaData()

users = Table(
    "Users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("discord_id", Integer, nullable=False),
    Column("coins", Integer, nullable=False),
)

coinflips = Table(
    "coinflips",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("discord_id", Integer, nullable=False),
    Column("coins", Integer, nullable=False),
    Column("enemy_discord_id", Integer),
    Column("winning_discord_id", Integer),
    Column("completed", Boolean, default=False),
)

metadata.create_all(engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
