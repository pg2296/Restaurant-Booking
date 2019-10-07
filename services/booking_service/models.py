from booking_app import db
from datetime import datetime
from sqlalchemy import PrimaryKeyConstraint



class Restaurant(db.Model):

    __tablename__ = "Restaurant"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(240),nullable=False)
    contact = db.Column(db.Text,nullable=False)
    email= db.Column(db.Text,nullable=True)
    address=db.Column(db.Text,nullable=False)
    bookings = db.relationship("Booking",backref='restaurant_book',lazy='dynamic')
    tables=db.relationship("Tables",backref='restaurant_tables',lazy='dynamic')
    table_types=db.relationship("Table_type",backref='restaurant_types',lazy='dynamic')
    menus = db.relationship("Menu",backref='restaurant_menu',lazy='dynamic')

    def __init__(self,name,contact,email,address):
        self.name=name
        self.contact=contact
        self.email=email
        self.address=address



class Booking(db.Model):

    __tablename__= "Booking"

    id= db.Column(db.Integer,primary_key=True)
    restaurant_id = db.Column(db.Integer,db.ForeignKey('Restaurant.id'),nullable=False)
    date= db.Column(db.DateTime, default=datetime.utcnow,nullable=False)
    status = db.Column(db.String(8),nullable=False)
    no_of_persons=db.Column(db.Integer,nullable=False)
    selected_menu=db.Column(db.Text,nullable=True)
    payment_status = db.Column(db.String(13),nullable=False)
    payments = db.relationship('Payment',backref='booking',lazy='dynamic')
    booked_slot=db.Column(db.Integer,nullable=False)

    def __init__(self,id,restaurant_id,date,status,no_of_persons,selected_menu,payment_status,booked_slot):
        self.id=id
        self.restaurant_id=restaurant_id
        self.date=date
        self.status=status
        self.no_of_persons=no_of_persons
        self.selected_menu=selected_menu
        self.payment_status=payment_status
        self.booked_slot=booked_slot


class Payment(db.Model):
    __tablename__ = "Payment"

    transaction_id = db.Column(db.Integer,primary_key=True)
    booking_id = db.Column(db.Integer,db.ForeignKey("Booking.id"))
    amount=db.Column(db.Integer,nullable=False)
    status=db.Column(db.String(13),nullable=False)
    date= db.Column(db.DateTime, default=datetime.utcnow,nullable=False)

    def __init__(self,booking_id,amount,status,date):

        self.booking_id=booking_id
        self.amount=amount
        self.status=status
        self.date=date

class Tables(db.Model):
    __tablename__ = "Tables"

    id=db.Column(db.Integer,primary_key=True)
    restaurant_id=db.Column(db.Integer,db.ForeignKey('Restaurant.id'),nullable=False)
    table_type=db.Column(db.String(2),nullable=False)
    Availablity=db.relationship('Availablity',backref="table_availablity",lazy='dynamic')

    def __init__(self,restaurant_id,table_type):

        self.restaurant_id=restaurant_id
        self.table_type=table_type

class Availablity(db.Model):
    __tablename__="Availablity"

    id=db.Column(db.Integer,primary_key=True)
    table_id=db.Column(db.ForeignKey(Tables.id),nullable=False)
    booking_date=db.Column(db.DateTime)
    slots=db.Column(db.Text,nullable=False)

    def __init__(self,table_id,booking_date,slots):

        self.table_id=table_id
        self.booking_date=booking_date
        self.slots=slots




class Table_type(db.Model):

    __tablename__="Table_type"

    id=db.Column(db.Integer,primary_key=True)
    type = db.Column(db.String(2),nullable=False,)
    price = db.Column(db.Integer,nullable=False)
    restaurant_id=db.Column(db.Integer,db.ForeignKey('Restaurant.id'))






    def __init__(self,type,price,restaurant_id):

        self.type=type
        self.price=price
        self.restaurant_id=restaurant_id


class Menu(db.Model):

    __tablename__="Menu"

    id= db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),nullable=False)
    price=db.Column(db.Integer,nullable=False)
    restaurant_id=db.Column(db.Integer,db.ForeignKey('Restaurant.id'))

    def __init__(self,name,price,restaurant_id):

        self.name=name
        self.price=price
        self.restaurant_id=restaurant_id
