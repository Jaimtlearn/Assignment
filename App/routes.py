from App import app, db, login_manager, bcrypt
from flask import render_template, url_for, flash, redirect, request
from datetime import datetime
from App.models import Contact, User
from App.forms import ContactForm, SignupForm, LoginForm
from flask_login import current_user, logout_user, login_user, login_required

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html', title="Home Page")

@app.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(name=form.name.data, email=form.email.data, detail=form.details.data)
        db.session.add(contact)
        db.session.commit()
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('get_details'))
    return render_template('contact.html', title="Contact", form=form)

@app.route('/details')
@login_required
def get_details():
    query_result = Contact.query.all()
    return render_template('detail.html', title="Details", contacts=query_result, flag=True)

@app.route('/signup', methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignupForm()
    if form.validate_on_submit():
        hased_pwd = bcrypt.generate_password_hash(form.password.data, 10)
        user = User(username=form.username.data, email=form.email.data, password=hased_pwd)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form, title="SignUp")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        next_page = request.args.get('next')
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            print(next_page)
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form, title="Login")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))