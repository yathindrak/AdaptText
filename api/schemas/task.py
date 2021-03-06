from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

from ..connection.initializers import database
from ..models.task import Task


class TaskSchema(ModelSchema):
   class Meta(ModelSchema.Meta):
       fields = ('id', 'name', 'description', 'progress', 'model_path', 'date_created', 'user_id')
       model = Task
       sqla_session = database.session
   # id = fields.Number(required=True, dump_only=True)
   # name = fields.String(required=True)
   # description = fields.String(required=True)
   # progress = fields.Number(required=False)
   # model_path = fields.String(required=False)
   # date_created = fields.DateTime(required=True)
   # user_id = fields.Number(required=True)