from datetime import datetime

from .metainfo import MetaInfo
from ..connection.initializers import database as db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.Text)
    progress = db.Column(db.Integer)
    model_path = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    meta_data = db.relationship(MetaInfo, backref='task', lazy=True, uselist=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # task = db.relationship('Task', back_populates='metadataa')
