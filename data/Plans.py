import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Plans(SqlAlchemyBase):
    __tablename__ = 'plans'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_owner = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    descreption = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_privated = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    user = orm.relationship("User")
