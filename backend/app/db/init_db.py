from sqlalchemy import create_engine
from app.core.config import settings
from app.db.models import Base

def init():
    engine = create_engine(settings.database_url)
    Base.metadata.create_all(engine)
    print("Base de datos inicializada.")

if __name__ == "__main__":
    init()
