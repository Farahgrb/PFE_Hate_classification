from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import dotenv_values
env_vars = dotenv_values()



from utils.util import Singleton

DATABASE_URL = "postgresql://{}:{}@{}:5432/{}".format(env_vars["POSTGRES_DB"],env_vars["POSTGRES_USER"],env_vars["POSTGRES_HOSTNAME"],env_vars["POSTGRES_PASSWORD"])


class Database(metaclass=Singleton):
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def get_session(self):
        return self.session()
    
db_class=Database()