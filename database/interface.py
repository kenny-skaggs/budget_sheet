
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, joinedload

from database import models as db_models
import models


class _DbConnection:
    def __init__(self):
        self.engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5432/budget')
        
class Interface:
    @classmethod
    def init_tables(cls):
        connection = _DbConnection()
        db_models.Base.metadata.create_all(connection.engine)
        
class DomainMapper:
    @classmethod
    def map_categorizer(cls, db_rule: db_models.Categorizer) -> models.Categorizer:
        result = models.Categorizer(
            pattern=db_rule.desc_pattern,
            category=models.Category(
                name=db_rule.category.name,
                is_external=db_rule.category.is_external
            )
        )
        if db_rule.amount_dollars or db_rule.amount_cents:
            result.amount = models.Amount(
                dollars=db_rule.amount_dollars,
                cents=db_rule.amount_cents
            )
            
        return result
        
class Repository:
    @classmethod
    def load_category_rules(cls):
        connection = _DbConnection()
        with Session(connection.engine) as session:
            stmt = select(db_models.Categorizer).options(
                joinedload(db_models.Categorizer.category)
            )
            return [
                DomainMapper.map_categorizer(db_rule)
                for db_rule in session.scalars(stmt)
            ]
