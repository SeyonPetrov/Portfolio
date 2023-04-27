import datetime
import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Files(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'file'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    owner = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    user_id = sqlalchemy.Column(sqlalchemy.Integer)
    type_f = sqlalchemy.Column(sqlalchemy.String, default='PDF')
    url_address = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    type = sqlalchemy.Column(sqlalchemy.String, default='Спорт')
    info = sqlalchemy.Column(sqlalchemy.String, default='Название')
    user = orm.relationship('User')

    def __repr__(self):
        return f'<Job> {self.url_address} {self.owner} {self.user_id}'
