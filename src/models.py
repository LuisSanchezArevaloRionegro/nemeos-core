from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey

db = SQLAlchemy()

user_workout = db.Table(
    'user_workout',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('workout_id', db.Integer, db.ForeignKey('workouts.id'), primary_key=True)
)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    deleted = db.Column(db.Boolean(), nullable=False, default=False)
    workouts = relationship('Workout', secondary=user_workout, back_populates='users')
    form = relationship("Form", uselist=False, back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "deleted": self.deleted,
            # do not serialize the password, its a security breach
        }
    def save(self):
        db.session.add(self)  
        db.session.commit()
        return self

    @classmethod
    def get_id(cls, email):
        return db.session.query(cls).filter(cls.email==email).first()

    @classmethod
    def get_name(cls, name):
        return db.session.query(cls).filter(cls.name==name).first()    

    @classmethod
    def get_all(cls):
        return db.session.query(cls).all()

    @classmethod
    def is_authenticated(self):
        return True

class Form(db.Model):
    __tablename__ = 'form'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    age = db.Column(db.Integer, nullable=False)
    dedication = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey("goals.id"))
    deleted = db.Column(db.Boolean(), nullable=False, default=False)
    user = relationship("User", back_populates="form")
    goals = relationship("Goal", back_populates="form")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "age": self.age,
            "dedication": self.dedication,
            "height": self.height,
            "weight": self.weight,
            "goal_id": self.goal_id,
            "deleted": self.deleted,
        }

class Workout(db.Model):
    __tablename__ = 'workouts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    intensity = db.Column(db.Integer, nullable=False)
    deleted = db.Column(db.Boolean(), nullable=False, default=False)
    users = relationship('User', secondary=user_workout, back_populates='workouts')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "intensity": self.intensity,
            "deleted": self.deleted,
        }

exercise_workout = db.Table('exercise_workout',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('exercise_id', db.Integer, db.ForeignKey('exercises.id')),
    db.Column('workout_id', db.Integer, db.ForeignKey('workouts.id'))
)

class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    name_en = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=False)
    deleted = db.Column(db.Boolean(), nullable=False, default=False)
    material = relationship("Material", uselist=False, back_populates="exercises")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_en": self.name_en,
            "deleted": self.deleted,
        }

class Goal(db.Model):
    __tablename__ = 'goals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    deleted = db.Column(db.Boolean(), nullable=False, default=False)
    form = relationship('Form', back_populates='goals', uselist=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "deleted": self.deleted,
        }

class Material(db.Model):
    __tablename__ = 'material'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    exercise_id = Column(Integer, ForeignKey('exercises.id'))
    deleted = db.Column(db.Boolean(), nullable=False, default=False)
    exercises = relationship("Exercise", back_populates="material")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "deleted": self.deleted,
        }
# TODO: Crear tabla de tiempos asociada a los ejercicios