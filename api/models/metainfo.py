from ..connection.initializers import database as db


class MetaInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ds_path = db.Column(db.Text)
    ds_text_col = db.Column(db.String(50))
    ds_label_col = db.Column(db.String(50))
    continuous_train = db.Column(db.Boolean, nullable=False)
    classes = db.Column(db.ARRAY(db.String))
    accuracy = db.Column(db.Float)
    err = db.Column(db.Float)
    xlim = db.Column(db.ARRAY(db.Float))
    ylim = db.Column(db.ARRAY(db.Float))
    fpr = db.Column(db.ARRAY(db.Float))
    tpr = db.Column(db.ARRAY(db.Float))
    roc_auc = db.Column(db.Float)
    roc_curve = db.Column(db.Text)
    conf_matrix = db.Column(db.Text)
    macro_f1 = db.Column(db.Float)
    macro_precision = db.Column(db.Float)
    macro_recall = db.Column(db.Float)
    macro_support = db.Column(db.Float)
    weighted_f1 = db.Column(db.Float)
    weighted_precision = db.Column(db.Float)
    weighted_recall = db.Column(db.Float)
    weighted_support = db.Column(db.Float)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

