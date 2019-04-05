from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from models.user import User
from models.image import Image
from flask_login import current_user, login_required
from config import Config
import helpers
import re
import datetime

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')

@images_blueprint.route('/upload', methods=['POST'])
@login_required
def create():
    user = User.get_by_id(current_user.id)
    username = user.username
    file = request.files.get('upload_pic')

    if "upload_pic" not in request.files or file.filename == "":
        flash('Please select a picture for upload')

    if file and helpers.allowed_file(file.filename):
        file.filename = secure_filename(f"feed_{str(datetime.datetime.now())}_{file.filename}")
        output = helpers.upload_file_to_s3(file, Config.S3_BUCKET)

        Image.create(user_id=current_user.id, image_url=file.filename)

        return redirect(url_for('users.show', username=username))
    else:
        return redirect(url_for('users.show', username=username))

