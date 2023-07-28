from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



from utils.util import Singleton

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/postgres"


class Database(metaclass=Singleton):
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def get_session(self):
        return self.session()
    
db_class=Database()