from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
#sqlalchemy is popular type of ORM that allows us to define our own table as python models
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}: {settings.database_port}/{settings.database_name}"


engine = create_engine (SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db(): #is a function that responds to every request in the db and close it when we are done
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
    
#     try:
#         conn = psycopg2.connect (host="localhost", database="fastapi",user="postgres",password="fathela123",
#                              cursor_factory= RealDictCursor)
#         cursor = conn.cursor()
#         print("connection to database successfull!!!")
#         break

#     except Exception as error:
#         print("connecting to database failed!!!")
#         print("Error:", error)
#         time.sleep(3)



