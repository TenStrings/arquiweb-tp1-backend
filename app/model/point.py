import uuid
from bson import ObjectId
class Point:

    def __init__(self, position, name, description, image,
                 categoryId, categoryName):
        self.position = position
        self.name = name
        self.description = description
        self.image = image
        self.categoryId = ObjectId(categoryId)
        self.categoryName = categoryName
        self.visible = True
        self.extern = False
        self.provider = dict(name='Jugo-Maps', site_url="https://jugo-maps.herokuapp.com")

#Because we are using mongo db _id and it is generated after we put them in the db
class ExternPoint:
    def __init__(self, position, name, description, image,
                 categoryId, categoryName, provider):
        self._id = uuid.uuid4().hex
        self.position = position
        self.name = name
        self.description = description
        self.image = image
        self.categoryId = categoryId
        self.categoryName = categoryName
        self.visible = True
        self.extern = True
        self.provider = provider
