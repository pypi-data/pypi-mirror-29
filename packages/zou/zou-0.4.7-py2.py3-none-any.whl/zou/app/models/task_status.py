from zou.app import db
from zou.app.models.serializer import SerializerMixin
from zou.app.models.base import BaseMixin


class TaskStatus(db.Model, BaseMixin, SerializerMixin):
    name = db.Column(db.String(40), nullable=False)
    short_name = db.Column(db.String(10), unique=True, nullable=False)
    color = db.Column(db.String(7), nullable=False)
    is_reviewable = db.Column(db.Boolean(), default=False)
    shotgun_id = db.Column(db.Integer)
