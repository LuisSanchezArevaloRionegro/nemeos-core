from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=True)
    last_name = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(80), nullable=True)
    password = db.Column(db.String(80), nullable=True)
    deleted = db.Column(db.Boolean(), nullable=True, default=False)

    def __repr__(self):
        return '<User %r>' % self.username

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
    def get_all(cls):
        return db.session.query(cls).all()

    @classmethod
    def is_authenticated(self):
        return True

class Form(db.Model):
    __tablename__ = 'form'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    deleted = db.Column(db.Boolean(), nullable=False, default=False)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "weight": self.weight,
            "height": self.height,
            "age": self.age,
            # do not serialize the password, its a security breach
        }

class Workout(db.Model):
    __tablename__ = 'workout'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    intensity = db.Column(db.Integer, nullable=False)
    deleted = db.Column(db.Boolean(), nullable=False, default=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "intensity": self.intensity,
            "deleted": self.deleted,
            # do not serialize the password, its a security breach
        }


class UserWorkoutRelation(db.Model):
    __tablename__ = 'user_workout_relation'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    workout_id = db.Column(db.Integer, db.ForeignKey("workout.id"))

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "workout_id": self.wworkout_ideight,
            # do not serialize the password, its a security breach
        }

class Exercise(db.Model):
    __tablename__ = 'exercise'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    deleted = db.Column(db.Boolean(), nullable=False, default=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "deleted": self.deleted,
            # do not serialize the password, its a security breach
        }

class WorkoutExerciseRelation(db.Model):
    __tablename__ = 'workout_exercise_relation'
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workout.id"))
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise.id"))

    def serialize(self):
        return {
            "id": self.id,
            "workout_id": self.workout_id,
            "exercise_id": self.exercise_id,
            # do not serialize the password, its a security breach
        }