
import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    ...
    
class Category(Base):
    __tablename__ = 'category'
    
    id = mapped_column(sa.Integer, primary_key=True)
    name = mapped_column(sa.String(64))
    is_external = mapped_column(sa.Boolean())
    
class Transaction(Base):
    __tablename__ = 'transaction'
    
    id = mapped_column(sa.Integer, primary_key=True)
    date = mapped_column(sa.Date())
    real_description = mapped_column(sa.String(256))
    amount_dollars = mapped_column(sa.Integer)
    amount_cents = mapped_column(sa.Integer)
    
    category_id = mapped_column(sa.ForeignKey(Category.id))
    category: Mapped[Category] = relationship()
    
class Categorizer(Base):
    __tablename__ = 'categorizer'
    
    id = mapped_column(sa.Integer, primary_key=True)
    desc_pattern = mapped_column(sa.String(512))
    amount_dollars = mapped_column(sa.Integer())
    amount_cents = mapped_column(sa.Integer())
    
    category_id = mapped_column(sa.ForeignKey(Category.id))
    category: Mapped[Category] = relationship()
