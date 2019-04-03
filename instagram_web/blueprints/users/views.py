from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models.user import User
from models.image import Image
from flask_login import current_user, login_required
from config import Config
import helpers
import re
from datetime import date

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')

@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')

@users_blueprint.route('/', methods=['POST'])
def create():
    if not re.search(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{6,})', request.form.get('new_password')):
        return render_template('users/new.html', errors=["Password must be at least 6 chars long, contain at least 1 capital letter, number, & symbol."])
    new_pw_hashed = generate_password_hash(request.form.get('new_password'))
    u = User(username=request.form.get('new_username'),
            first_name=request.form.get('new_firstname'),
            last_name=request.form.get('new_lastname'),
            email=request.form.get('new_email'),
            password=new_pw_hashed)

    if u.save():
        flash("New user created.")
        return redirect(url_for('users.new'))
    else:
        flash("Failed to create new user. Try again?")
        return render_template('users/new.html', errors=u.errors)







# UNDER CONSTRUCTION
# -------------------------------------------------------------------------

@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    return render_template('users/profile.html', username=username)







@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"



# -------------------------------------------------------------------------








@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User.get_by_id(id)

    if current_user == user:
        return render_template('users/edit.html', user=user)
    else:
        return render_template('home', errors=['Log in to access this page.'])

@users_blueprint.route('/<id>/edit/submit', methods=['POST'])
@login_required
def update(id):
    user = User.get_by_id(id)
    if not "" and re.search(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{6,})', request.form.get('change_password')):
        return render_template('users/edit.html', errors=["Password must be at least 6 chars long, contain at least 1 capital letter, number, & symbol."])
        # return redirect(url_for('users.edit',  id=current_user.id, errors=['Invalid password']))
    change_pw_hashed = generate_password_hash(request.form.get('change_password'))

    if current_user == user:
        user.first_name = request.form.get('change_firstname')
        user.last_name = request.form.get('change_lastname')

        user.password = change_pw_hashed
        user.email = request.form.get('change_email')

        if user.save():
            return redirect(url_for('users.edit', id=current_user.id))
        else:
            # return redirect(url_for('users.edit',  id=current_user.id, errors=user.errors))
            return render_template('users/edit.html', id=current_user.id, errors=user.errors)

    else:
        return render_template('home.html', errors=['Log in to access this page.'])

@users_blueprint.route('/<id>/edit/upload', methods=['POST'])
@login_required
def upload(id):
    user = User.get_by_id(id)
    file = request.files.get('user_pic')
    # if "user_pic" not in request.files:
    #     flash file.filename == "" or
    if "user_pic" not in request.files or file.filename == "":
        flash('Please select a picture for upload')
    if file and helpers.allowed_file(file.filename):
        file.filename = secure_filename(f"{str(id)}_{str(date.today())}_{file.filename}")
        output = helpers.upload_file_to_s3(file, Config.S3_BUCKET)
        user.profile_pic = file.filename
        user.save()
        # return str(output)
        return redirect(url_for('users.edit', id=id))
    else:
        return redirect(url_for('users.edit', id=id))



    # pass
    # flash('this button is working')
    # return render_template('users/edit.html', id=current_user.id)
    # file = request.files.get('user_pic')
    # if file:
    #     file.filename = secure_filename(file.filename)



    # s3_resource = boto3.resource('s3')
    # my_bucket = s3_resource.Bucket(S3_BUCKET)
    # my_bucket.Object(file.filename).put(Body=file)

    # flash('File uploaded successfully')
    # return redirect(url_for('users.edit', id=current_user.id))

# ALLOW EXTENSIONS SOMEWHERE HERE