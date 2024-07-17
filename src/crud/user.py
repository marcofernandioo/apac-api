from models.Record import Record

from sqlalchemy import create_engine, inspect, Table, MetaData, column, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from typing import List, Dict, Any, Optional

from sqlalchemy import select

from . import execute_query

def get_all_records(db: Session, table_name: str) -> List[Dict[str, Any]]:
    return execute_query(db, table_name)

def get_user_by_username(db: Session, username: str) -> Optional[Dict[str, Any]]:
    filter_condition = f"username = :username"
    result = db.execute(select(Table("users", MetaData(), autoload_with=db.get_bind())).where(text(filter_condition)), {"username": username})
    # users = [dict(row) for row in result]
    # return users[0] if users else None
    return result
