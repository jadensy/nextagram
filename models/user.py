from models.base_model import BaseModel
import peewee as pw
import os
from flask_login import UserMixin
from peewee_validates import ModelValidator, validate_email, StringField
from playhouse.hybrid import hybrid_property
from config import Config


class User(BaseModel, UserMixin):
    first_name = pw.CharField()
    last_name = pw.CharField(null=True)
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()
    profile_pic = pw.CharField(null=True)
    private = pw.BooleanField(default=0)

    @hybrid_property
    def profile_image_url(self):
        profile_pic = self.profile_pic
        if not profile_pic:
            return f"{Config.S3_LOCATION}_placeholder.jpg"
        else:
            return f"{Config.S3_LOCATION}{self.id}/{self.profile_pic}"

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)

        if duplicate_username and not duplicate_username.id == self.id:
            self.errors.append('Username has been registered. Please try another.')
        elif duplicate_email and not duplicate_email.id == self.id:
            self.errors.append('Email has been registered. Please try another.')

    def save(self, *args, **kwargs):
        self.errors = []
        self.validate()
        validator = self.CustomValidator(self)
        validator.validate()

        if validator.errors != 0:
            for error in validator.errors.values():
                self.errors.append(error)

        if len(self.errors) == 0:
            self.updated_at = datetime.datetime.now()
            return super(BaseModel, self).save(*args, **kwargs)
        else:
            return 0

    class CustomValidator(ModelValidator):
        first_name = StringField(required=True)
        username = StringField(required=True)
        email = StringField(required=True,validators=[validate_email()])
        password = StringField(required=True)

        class Meta:
            messages = {
                "email.validators": "Email address is invalid.",
                "required": "This field is required."
            }
