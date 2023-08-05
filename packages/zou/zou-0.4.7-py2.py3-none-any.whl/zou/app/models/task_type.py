from sqlalchemy_utils import UUIDType

from zou.app import db
from zou.app.models.serializer import SerializerMixin
from zou.app.models.base import BaseMixin


class TaskType(db.Model, BaseMixin, SerializerMixin):
    name = db.Column(db.String(40), nullable=False)
    color = db.Column(db.String(7), default="#FFFFFF")
    priority = db.Column(db.Integer, default=1)
    for_shots = db.Column(db.Boolean, default=False)
    shotgun_id = db.Column(db.Integer)

    department_id = \
        db.Column(
            UUIDType(binary=False),
            db.ForeignKey("department.id")
        )

    __table_args__ = (
        db.UniqueConstraint(
            'name',
            'department_id',
            name='task_type_uc'
        ),
    )
