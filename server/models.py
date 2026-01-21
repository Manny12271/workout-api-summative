from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint
from datetime import date

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )

    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        viewonly=True
    )

    __table_args__ = (
        CheckConstraint("length(name) >= 2", name="exercise_name_min_len"),
        CheckConstraint("length(category) >= 2",
                        name="exercise_category_min_len"),
    )

    @validates("name")
    def validate_name(self, key, value):
        if value is None:
            raise ValueError("Exercise name is required.")
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Exercise name must be at least 2 characters.")
        return value

    @validates("category")
    def validate_category(self, key, value):
        if value is None:
            raise ValueError("Category is required.")
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Category must be at least 2 characters.")
        return value


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )

    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        viewonly=True
    )

    __table_args__ = (
        CheckConstraint("duration_minutes > 0",
                        name="workout_duration_positive"),
    )

    @validates("duration_minutes")
    def validate_duration_minutes(self, key, value):
        if value is None:
            raise ValueError("duration_minutes is required.")
        if not isinstance(value, int):
            raise ValueError("duration_minutes must be an integer.")
        if value <= 0:
            raise ValueError("duration_minutes must be greater than 0.")
        return value

    @validates("date")
    def validate_date(self, key, value):
        if value is None:
            raise ValueError("date is required.")
        if not isinstance(value, date):
            raise ValueError("date must be a valid date.")
        return value


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey(
        "workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey(
        "exercises.id"), nullable=False)

    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    __table_args__ = (
        CheckConstraint("reps IS NULL OR reps > 0", name="reps_positive"),
        CheckConstraint("sets IS NULL OR sets > 0", name="sets_positive"),
        CheckConstraint("duration_seconds IS NULL OR duration_seconds > 0",
                        name="duration_seconds_positive"),
    )

    @validates("reps")
    def validate_reps(self, key, value):
        if value is None:
            return None
        if not isinstance(value, int):
            raise ValueError("reps must be an integer.")
        if value <= 0:
            raise ValueError("reps must be greater than 0.")
        return value

    @validates("sets")
    def validate_sets(self, key, value):
        if value is None:
            return None
        if not isinstance(value, int):
            raise ValueError("sets must be an integer.")
        if value <= 0:
            raise ValueError("sets must be greater than 0.")
        return value

    @validates("duration_seconds")
    def validate_duration_seconds(self, key, value):
        if value is None:
            return None
        if not isinstance(value, int):
            raise ValueError("duration_seconds must be an integer.")
        if value <= 0:
            raise ValueError("duration_seconds must be greater than 0.")
        return value
