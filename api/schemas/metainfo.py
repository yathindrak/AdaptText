from marshmallow_sqlalchemy import ModelSchema

from ..connection.initializers import database
from ..models.metainfo import MetaInfo


class MetaInfoSchema(ModelSchema):
   class Meta(ModelSchema.Meta):
       fields = ('id', 'ds_path', 'ds_text_col', 'ds_label_col', 'continuous_train', 'accuracy', 'task_id')
       model = MetaInfo
       sqla_session = database.session