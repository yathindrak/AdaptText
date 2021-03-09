from marshmallow_sqlalchemy import ModelSchema

from ..connection.initializers import database
from ..models.task import Task


class TaskSchema(ModelSchema):
   class Meta(ModelSchema.Meta):
       fields = ('id', 'name', 'description', 'progress', 'model_path', 'date_created', 'user_id',
                 'meta_data.ds_path', 'meta_data.ds_text_col','meta_data.ds_label_col', 'meta_data.accuracy', 'meta_data.err')
       model = Task
       sqla_session = database.session