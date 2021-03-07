from ..connection.initializers import database as db


class MetaInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ds_path = db.Column(db.Text)
    ds_text_col = db.Column(db.String(50))
    ds_label_col = db.Column(db.String(50))
    continuous_train = db.Column(db.Boolean, nullable=False)
    accuracy = db.Column(db.Float)
    err = db.Column(db.Float)
    roc_auc = db.Column(db.Float)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
