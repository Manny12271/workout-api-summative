#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Workout, Exercise, WorkoutExercise


def seed():
    db.drop_all()
    db.create_all()

    squat = Exercise(name="Squat", category="Strength", equipment_needed=True)
    bench = Exercise(name="Bench Press", category="Strength",
                     equipment_needed=True)
    jumping_jacks = Exercise(name="Jumping Jacks",
                             category="Cardio", equipment_needed=False)
    plank = Exercise(name="Plank", category="Core", equipment_needed=False)

    w1 = Workout(date=date.today(), duration_minutes=60,
                 notes="Full body strength")
    w2 = Workout(date=date.today(), duration_minutes=30,
                 notes="Quick conditioning")

    db.session.add_all([squat, bench, jumping_jacks, plank, w1, w2])
    db.session.commit()

    we1 = WorkoutExercise(
        workout_id=w1.id, exercise_id=squat.id, sets=5, reps=5)
    we2 = WorkoutExercise(
        workout_id=w1.id, exercise_id=bench.id, sets=5, reps=5)
    we3 = WorkoutExercise(
        workout_id=w2.id, exercise_id=jumping_jacks.id, duration_seconds=120)
    we4 = WorkoutExercise(
        workout_id=w2.id, exercise_id=plank.id, duration_seconds=60)

    db.session.add_all([we1, we2, we3, we4])
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        seed()
        print("✅ Database seeded successfully!")
