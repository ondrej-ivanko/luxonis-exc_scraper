from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from luxonis_sreality.db_engine import engine

Base = declarative_base()


class AparmentsForSale(Base):
    __tablename__ = "apartments_sale"

    id = Column(Integer(), primary_key=True)
    title = Column(String(255), nullable=False, unique=True)
    img_url = Column(String(255), nullable=False, unique=True)


Base.metadata.create_all(engine)
