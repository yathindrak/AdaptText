from marshmallow_sqlalchemy import ModelSchema

from ..connection.initializers import database
from ..models.task import Task


class TaskSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        """Manage a Task"""
        fields = ('id', 'name', 'description', 'progress', 'model_path', 'date_created', 'user_id',
                  'meta_data.ds_path', 'meta_data.ds_text_col', 'meta_data.ds_label_col', 'meta_data.classes',
                  'meta_data.accuracy',
                  'meta_data.err', 'meta_data.roc_curve', 'meta_data.conf_matrix', 'meta_data.macro_f1',
                  'meta_data.macro_precision', 'meta_data.macro_recall', 'meta_data.macro_support',
                  'meta_data.weighted_f1', 'meta_data.weighted_precision',
                  'meta_data.weighted_recall', 'meta_data.weighted_support', 'meta_data.matthews_corr_coef')

        model = Task
        sqla_session = database.session
