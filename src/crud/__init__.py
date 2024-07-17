from sqlalchemy import inspect, Table, MetaData, column, text
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, Session


def execute_query(db: Session, table_name: str, filter_condition=None):
    try:
        engine = db.get_bind()
        metadata = MetaData()
        table = Table(table_name, metadata, autoload_with=engine)

        stmt = select(table)
        if filter_condition:
            stmt = stmt.where(text(filter_condition))

        if params:
            result = db.execute(stmt, params)
        else:
            print('no pp')
            result = db.execute(stmt)

        records = [dict(zip(result.keys(), row)) for row in result.fetchall()]
        return records
    except Exception as e:
        print(f"An error occurred: {e}")
        return []