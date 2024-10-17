import json
from datetime import datetime
from urllib.parse import quote_plus

import uuid as uuid
from pytz import timezone
from sqlalchemy import Column, TIMESTAMP, Boolean, Integer, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from sqlalchemy.sql import text

from config.settings import DB
import logging
# from logger import logging

DBTYPE_POSTGRES = "postgresql"
CORE_SQLALCHEMY_DATABASE_URI = "%s://%s:%s@%s:%s/%s" % (
    DBTYPE_POSTGRES,
    DB.user,
    quote_plus(DB.pass_),
    DB.host,
    DB.port,
    DB.name,
)

db_engine = create_engine(CORE_SQLALCHEMY_DATABASE_URI)

logger = logging.getLogger(__name__)
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

UTC = timezone("UTC")


def time_now():
    return datetime.now(UTC)


DBBase = declarative_base()


def get_db():
    """this function is used to inject db_session dependency in every rest api requests"""
    from controller.context_manager import context_set_db_session_rollback

    db: Session = SessionLocal()
    try:
        yield db
        #  commit the db session if no exception occurs
        #  if context_set_db_session_rollback is set to True then rollback the db session
        if context_set_db_session_rollback.get():
            logging.info("rollback db session")
            db.rollback()
        else:
            db.commit()
    except Exception as e:
        #  rollback the db session if any exception occurs
        logging.error(e)
        db.rollback()
    finally:
        #  close the db session
        db.close()


def get_test():
    db: Session = SessionLocal()

    a = db.execute(text("select * from test"))
    ans = a.fetchall()

    # Convert datetime.time objects to strings
    ans_list = []
    for row in ans:
        ans_list.append([row[0], row[1].strftime("%H:%M:%S")])

    return ans_list


def get_monthly_payment_by_cardid(userID: str):
    db: Session = SessionLocal()
    a = db.execute(
        text("select * from monthly_payment where card_id = :card_id"),
        {"card_id": userID},
    )
    ans = a.fetchall()
    return ans

    
