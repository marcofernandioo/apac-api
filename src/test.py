from models.Record import Record

from sqlalchemy import create_engine, inspect, Table, MetaData, column, text

from typing import List, Dict, Any, Optional

from sqlalchemy import select

from crud.user import get_all_records, get_user_by_username


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db = get_db()

def get_all_users_1(db: Session):
    try:
        # Create a select statement
        stmt = select(users)
        
        # Execute the query and fetch all results
        users = db.execute(stmt).scalars().all()
        
        return users
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
def get_all_records_1(db: Session, table_name: str):
    try:
        # Get the engine from the session
        engine = db.get_bind()
        # Create a MetaData instance
        metadata = MetaData()
        # Reflect the table
        table = Table(table_name, metadata, autoload_with=engine)
        # Create a select statement
        stmt = select(table)
        # Execute the query and fetch all results
        result = db.execute(stmt)
        # Fetch all rows
        records = result.fetchall()

        return records
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    


with SessionLocal() as db:
    # Get all users
    # all_users = get_all_records(db, "users")
    # print("All users:")
    # for user in all_users:
    #     print(user)
    # # Get user by username
    # username = "john_doe"
    # user = get_user_by_username(db, username)
    # if user:
    #     print(f"\nFound user: {user}")
    # else:
    #     print(f"\nUser '{username}' not found")
    res = get_all_records(db, "users");
    # res = get_user_by_username(db, "john_doe")
    print(res)

    