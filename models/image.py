import os
import peewee as pw
from models.base_model import BaseModel
from models.user import User
from playhouse.hybrid import hybrid_property
from config import Config

class Image(BaseModel):
    user_id = pw.ForeignKeyField(User, backref='images')
    image_url = pw.CharField()
    caption = pw.TextField(null=True)

    @hybrid_property
    def feed_image_url(self):
        return f"{Config.S3_LOCATION}{self.user_id}/{self.image_url}"
