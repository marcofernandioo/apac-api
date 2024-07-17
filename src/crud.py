
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
            result = db.execute(stmt)

        records = [dict(zip(result.keys(), row)) for row in result.fetchall()]
        return records
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_all_records(db: Session, table_name: str) -> List[Dict[str, Any]]:
    return execute_query(db, table_name)

def get_user_by_username(db: Session, username: str) -> Optional[Dict[str, Any]]:
    filter_condition = f"username = :username"
    result = db.execute(select(Table("users", MetaData(), autoload_with=db.get_bind())).where(text(filter_condition)), {"username": username})
    # users = [dict(row) for row in result]
    # return users[0] if users else None
    return result
