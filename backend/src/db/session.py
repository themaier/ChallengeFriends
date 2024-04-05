from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlmodel import Session, SQLModel
import os
from dotenv import load_dotenv

# db_model import is important for creating the tables in postgres
from src.db_models import *
from src.db_models.challenges import ChallengeTable
from src.db_models.friends import FriendsTable
from src.db_models.hashtags import HashtagTable
from src.db_models.text_reaction import TextReactionTable
from src.db_models.users import UserTable


# private
def __get_engine(user, passwd, host, port, db):
    url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
    print(url)
    if not database_exists(url):
        create_database(url)
        # --------------------------------------------
        # echo -> print all SQL statements to console
        # ---------------------------------------|----
    engine = create_engine(url, pool_size=50, echo=True)
    return engine


# private
def __get_engine_from_settings():
    load_dotenv(dotenv_path=".env")
    # if not specified in docker-compose file -> localhost
    pghost = os.getenv("POSTGRES_HOSTNAME", "localhost")
    pguser = os.getenv("POSTGRES_USERNAME")
    pgpasswd = os.getenv("POSTGRES_PASSWORD")
    pgport = os.getenv("POSTGRES_PORT")
    pgdb = os.getenv("POSTGRES_DB_NAME")
    return __get_engine(pguser, pgpasswd, pghost, pgport, pgdb)


# ----------public-----------
engine = __get_engine_from_settings()


def get_db():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


def init_db() -> None:
    SQLModel.metadata.create_all(engine)
