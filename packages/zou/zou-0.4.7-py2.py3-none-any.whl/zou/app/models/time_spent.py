from sqlalchemy_utils import UUIDType
from zou.app import db
from zou.app.models.serializer import SerializerMixin
from zou.app.models.base import BaseMixin


class TimeSpent(db.Model, BaseMixin, SerializerMixin):
    duration = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)

    task_id = \
        db.Column(UUIDType(binary=False), db.ForeignKey('task.id'))
    person_id = \
        db.Column(UUIDType(binary=False), db.ForeignKey('person.id'))

    __table_args__ = (
        db.UniqueConstraint(
            'person_id',
            'task_id',
            'date',
            name='time_spent_uc'
        ),
    )
