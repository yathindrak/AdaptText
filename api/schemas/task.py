from marshmallow_sqlalchemy import ModelSchema

from ..connection.initializers import database
from ..models.task import Task


class TaskSchema(ModelSchema):
   class Meta(ModelSchema.Meta):
       fields = ('id', 'name', 'description', 'progress', 'model_path', 'date_created', 'user_id')
       model = Task
       sqla_session = database.session