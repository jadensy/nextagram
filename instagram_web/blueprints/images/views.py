from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from models.user import User
from models.image import Image
from flask_login import current_user, login_required
from config import Config
import helpers
import re
from datetime import date

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')

@images_blueprint.route('/upload', methods=['POST'])
@login_required
def create():
    user = User.get(User.username==username)
    file = request.files.get('upload_pic')

    if "upload_pic" not in request.files or file.filename == "":
        flash('Please select a picture for upload')

    if file and helpers.allowed_file(file.filename):
        file.filename = secure_filename(f"{str(date.today())}_{file.filename}")
        output = helpers.upload_file_to_s3(file, Config.S3_BUCKET)

        # user.profile_pic = file.filename
        # user.save()

        return redirect(url_for('users.edit', id=id))
    else:
        return redirect(url_for('users.edit', id=id))

