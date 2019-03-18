from datetime import datetime
from clients import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    region = db.Column(db.String(100), unique=False, nullable=False)
    company_name = db.Column(db.String(50), unique=True, nullable=False)
    specialization = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(50), unique=True, nullable=False)
    company_data = db.Column(db.Text(500), unique=False, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"Customer('{self.region}', '{self.company_name}', '{self.specialization}', '{self.image_file}')"