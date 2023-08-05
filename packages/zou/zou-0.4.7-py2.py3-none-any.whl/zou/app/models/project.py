from sqlalchemy_utils import UUIDType
from sqlalchemy.dialects.postgresql import JSONB

from zou.app import db
from zou.app.models.serializer import SerializerMixin
from zou.app.models.base import BaseMixin


class Project(db.Model, BaseMixin, SerializerMixin):
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(200))
    shotgun_id = db.Column(db.Integer)
    file_tree = db.Column(JSONB)

    project_status_id = \
        db.Column(UUIDType(binary=False), db.ForeignKey('project_status.id'))
