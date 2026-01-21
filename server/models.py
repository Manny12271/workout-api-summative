from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)

    # Table constraint (1)
    __table_args__ = (
        CheckConstraint("length(name) >= 2", name="exercise_name_min_len"),
        CheckConstraint("length(category) >= 2",
                        name="exercise_category_min_len"),
    )

    # Model validations (2)
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
