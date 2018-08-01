from flask_security import RoleMixin, UserMixin
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy_continuum import make_versioned,  plugins
from passlib.hash import sha256_crypt
from datetime import datetime

db = SQLAlchemy()

#version
make_versioned( plugins=[plugins.FlaskPlugin()])
# User Role Association
user_roles = db.Table('user_roles',
                db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)

# Basic Class
class Base (object):
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=datetime.utcnow)

# User Model
class User(Base, db.Model, UserMixin):
    #version
    __versioned__ = {}
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # User fields
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    # User Authentication fields
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False, server_default='')
    # Trackable
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    confirmed_at = db.Column(db.DateTime(timezone=True))

    # Define the relationship to Role via UserRoles
    roles = db.relationship('Role', secondary=user_roles,lazy='subquery', backref=db.backref('users', lazy=True))

    tasks = db.relationship('Task', backref='user', lazy=True)

    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy='dynamic')
    messages_received = db.relationship('Message', foreign_keys='Message.recipient_id', backref='recipient', lazy='dynamic')

    def __str__(self):
        return self.firstname + ' '+ self.lastname

    def new_messages(self):
        return Message.query.filter_by(recipient=self).filter(Message.is_read == 0).count()

    def seen_message(self, id):
        msg = self.messages_received.filter_by(id=id).first()
        msg.is_read = 1
        db.session.add(msg)
        return msg

    def hash_password(self, password):
        self.password = sha256_crypt.hash(password)


# Define the Role data-model
class Role(db.Model, RoleMixin):
    #version
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __str__(self):
        return self.name


# Tasks Model
class Task (Base,db.Model):
    __tablename__='tasks'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    task_type_id = db.Column(db.Integer(), db.ForeignKey('tasks_type.id', ondelete='CASCADE'))
    task_type = db.relationship('TaskType', lazy=True)
    organization_id = db.Column(db.Integer(), db.ForeignKey('organizations.id', ondelete='CASCADE'))
    organization = db.relationship('Organization', lazy=True)
    place_id = db.Column(db.Integer(), db.ForeignKey('places.id', ondelete='CASCADE'))
    place = db.relationship('Place', lazy=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    results = db.Column(db.Text)

    def __repr__(self):
     return '{0}(id={1})'.format(self.__class__.__name__, self.id)

# TaskTypes Model
class TaskType(Base,db.Model):
    __tablename__='tasks_type'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __str__(self):
        return self.name

# Organizations Model
class Organization(Base,db.Model):
    __tablename__='organizations'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __str__(self):
        return self.name

# Places Model
class Place(Base,db.Model):
    __tablename__='places'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __str__(self):
        return self.name

# Pages Model
class Page(Base, db.Model):
    __tablename__='pages'
    id = db.Column(db.Integer(), primary_key=True)
    url = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text)
    publish = db.Column(db.Boolean(), nullable=True, server_default='0')
    publish_at = db.Column(db.DateTime, nullable=True)

# Messages Model
class Message(db.Model):
    __tablename__='messages'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('messages.id'))
    parent = db.relationship('Message', lazy=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    subject = db.Column(db.String(50))
    body = db.Column(db.String(140))
    is_read = db.Column(db.Boolean(), server_default='0')
    timestamp = db.Column(db.DateTime(timezone=True), index=True, default=datetime.utcnow())

    def __str__(self):
        return self.body



#map for version to create a model for them
sa.orm.configure_mappers()
