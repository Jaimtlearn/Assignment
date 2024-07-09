from App import app, db
from flask import render_template, url_for, flash, redirect
from datetime import datetime
from App.models import Contact
from App.forms import ContactForm

@app.route('/')
def home():
    return render_template('home.html', title="Home Page")

@app.route('/contact', methods=['GET', 'POST'])
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
def get_details():
    query_result = Contact.query.all()
    return render_template('detail.html', title="Details", contacts=query_result, flag=True)
