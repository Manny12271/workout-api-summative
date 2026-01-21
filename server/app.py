import os
from flask import Flask, request, make_response
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError

from models import db, Workout, Exercise, WorkoutExercise
from schemas import WorkoutSchema, ExerciseSchema, WorkoutExerciseSchema

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
    os.path.join(BASE_DIR, "app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)
db.init_app(app)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()


@app.get("/workouts")
def get_workouts():
    workouts = Workout.query.all()
    return make_response(workouts_schema.dump(workouts), 200)


@app.get("/workouts/<int:id>")
def get_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response({"error": "Workout not found"}, 404)
    return make_response(workout_schema.dump(workout), 200)


@app.post("/workouts")
def create_workout():
    data = request.get_json() or {}
    try:
        validated = workout_schema.load(data)
        workout = Workout(**validated)
        db.session.add(workout)
        db.session.commit()
        return make_response(workout_schema.dump(workout), 201)
    except Exception as e:
        db.session.rollback()
        return make_response({"error": str(e)}, 400)


@app.delete("/workouts/<int:id>")
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response({"error": "Workout not found"}, 404)
    db.session.delete(workout)
    db.session.commit()
    return make_response({}, 204)


@app.get("/exercises")
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(exercises_schema.dump(exercises), 200)


@app.get("/exercises/<int:id>")
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)

    data = exercise_schema.dump(exercise)
    data["workouts"] = [
        {"id": w.id, "date": w.date.isoformat(), "duration_minutes": w.duration_minutes}
        for w in exercise.workouts
    ]
    return make_response(data, 200)


@app.post("/exercises")
def create_exercise():
    data = request.get_json() or {}
    try:
        validated = exercise_schema.load(data)
        exercise = Exercise(**validated)
        db.session.add(exercise)
        db.session.commit()
        return make_response(exercise_schema.dump(exercise), 201)
    except IntegrityError:
        db.session.rollback()
        return make_response({"error": "Exercise name must be unique."}, 400)
    except Exception as e:
        db.session.rollback()
        return make_response({"error": str(e)}, 400)


@app.delete("/exercises/<int:id>")
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)
    db.session.delete(exercise)
    db.session.commit()
    return make_response({}, 204)


@app.post("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises")
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return make_response({"error": "Workout not found"}, 404)

    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)

    data = request.get_json() or {}

    payload = {
        "reps": data.get("reps"),
        "sets": data.get("sets"),
        "duration_seconds": data.get("duration_seconds"),
        "workout_id": workout_id,
        "exercise_id": exercise_id,
    }

    try:
        workout_exercise_schema.load(payload)

        we = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=payload["reps"],
            sets=payload["sets"],
            duration_seconds=payload["duration_seconds"],
        )

        db.session.add(we)
        db.session.commit()

        return make_response(
            {
                "message": "Exercise added to workout",
                "workout_exercise_id": we.id
            },
            201
        )

    except Exception as e:
        db.session.rollback()
        return make_response({"error": str(e)}, 400)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
