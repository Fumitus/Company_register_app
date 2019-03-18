import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from clients import app, db
from clients.forms import RegistrationForm, UpdatePostForm
from clients.models import Customer


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    page = request.args.get('page', 1, type=int)
    posts = Customer.query.order_by(Customer.input_date.desc()).paginate(page=page, per_page=5)
    image_file = url_for('static', filename='profile_pics/' + Customer.image_file)
    return render_template('home.html', posts=posts, image_file=image_file)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    output_size = (250, 250)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
        else:
            picture_file = None
        customer = Customer(region=form.region.data, 
                            company_name=form.company_name.data,
                            specialization=form.specialization.data,
                            email=form.email.data,
                            phone_number=form.phone_number.data,
                            company_data=form.company_data.data,
                            image_file=picture_file)
        db.session.add(customer)
        db.session.commit()
        
        flash('Data about company "{}" recorded to database.'.format(form.company_name.data), 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register',
                           form=form, legend='New Client')


@app.route("/register/<int:register_id>")
def update(register_id):
    post = Customer.query.get_or_404(register_id)
    return render_template('update.html', title=post.company_name, post=post)


@app.route("/register/<int:register_id>/update", methods=['GET', 'POST'])
def update_post(register_id):
    post = Customer.query.get_or_404(register_id)
    form = UpdatePostForm()
    if form.validate_on_submit():
        post.region = form.region.data
        post.company_name = form.company_name.data
        post.specialization = form.specialization.data
        post.email = form.email.data
        post.phone_number = form.phone_number.data
        post.company_data = form.company_data.data
        if form.picture.data:
            post.image_file = save_picture(form.picture.data)
        else:
            post.image_file
        db.session.commit()
        flash('Company data has been updated!', 'success')
        return redirect(url_for('update', register_id=post.id))
    elif request.method == 'GET':
        form.region.data = post.region
        form.company_name.data = post.company_name
        form.specialization.data = post.specialization
        form.email.data = post.email
        form.phone_number.data = post.phone_number
        form.company_data.data = post.company_data

    return render_template('register.html', title='Update data',
                           form=form, legend='Update data')


@app.route("/register/<int:register_id>/delete", methods=['POST'])
def delete_post(register_id):
    post = Customer.query.get_or_404(register_id)
    db.session.delete(post)
    db.session.commit()
    flash('Company "{}" data has been deleted!'.format(post.company_name), 'success')
    return redirect(url_for('home'))


@app.route("/region/<string:region>")
def town_companies(region):
    page = request.args.get('page', 1, type=int)
    town = Customer.query.filter_by(region=region).first_or_404()
    posts = Customer.query.filter_by(region=region)\
        .order_by(Customer.input_date.desc())\
        .paginate(page=page, per_page=5)
    image_file = url_for('static', filename='profile_pics/' + Customer.image_file)
    return render_template('town_companies.html', posts=posts, image_file=image_file, town=town)

