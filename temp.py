from App import app, db
from App.models import Contact

with app.app_context():
    contacts = Contact.query.all()

for contact in contacts:
    print(f"Id : {contact.id} Name: {contact.name} Email: {contact.email} Details: {contact.detail}")