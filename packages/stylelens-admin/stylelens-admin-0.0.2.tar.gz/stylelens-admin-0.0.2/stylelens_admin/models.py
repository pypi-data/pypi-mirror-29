from bson.objectid import ObjectId
from stylelens_admin.database import DataBase

class Models(DataBase):
  def __init__(self):
    super(Models, self).__init__()
    self.models = self.db.models

  def add_model(self, type, url, version):
    model = {}
    model['type'] = type
    model['url'] = url
    model['version'] = version

    query = {}
    query['type'] = type
    query['version'] = version
    try:
      r = self.models.update_one(query,
                                 {"$set": model},
                                 upsert=True)
    except Exception as e:
      print(e)

    model_id = None
    if 'upserted' in r.raw_result:
      model_id = str(r.raw_result['upserted'])

    return model_id

  def set_current_model(self, type, version):
    model = {}

    try:
      query = {}
      query['type'] = type
      model['use'] = False
      r = self.models.update_many(query,
                                 {"$set": model},
                                 upsert=False)

      query['version'] = version
      model['use'] = True
      r = self.models.update_one(query,
                                 {"$set": model},
                                 upsert=False)
    except Exception as e:
      print(e)

    return r.raw_result

  def get_current_model(self, type, version_id):
    query = {}
    query['type'] = type
    query['version_id'] = version_id
    try:
      r = self.models.find_one(query)
    except Exception as e:
      print(e)

    return r

  def get_models(self, type=None, offset=0, limit=100):
    query = {}

    if type != None:
      query['type'] = type

    try:
      r = self.models.find(query).skip(offset).limit(limit)
    except Exception as e:
      print(e)

    return list(r)
