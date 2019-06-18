import uuid
from app import mongo
class Category:

    def __init__(self, title, icon):
        self.title = title
        self.icon = icon
        self.visible = True
        self.extern = False
        self.provider = dict(name='Jugo-Maps', site_url='https://jugo-maps.herokuapp.com')


#Because we are using mongo db _id and it is generated after we put them in the db
class ExternCategory:
    def __init__(self, title, icon, provider):
        self._id = uuid.uuid4().hex
        self.title = title
        self.icon = icon
        self.extern = True
        self.provider = provider
        hidden_category = mongo.db.hidden_extern_categories.find_one({'abs_id':provider['cat_abs_id']})
        if hidden_category is None:
            self.visible = True
        else:
            self.visible = False
