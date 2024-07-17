from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pymysql

pymysql.install_as_MySQLdb()
 
# We can't use localhost if we're using docker.
db_url = "mysql+pymysql://root:root@host.docker.internal:3306/books_db"

engine = create_engine(db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()