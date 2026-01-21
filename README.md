# Workout API (Flask + SQLAlchemy + Marshmallow)

Backend API for a workout tracking application used by personal trainers. The API manages workouts, reusable exercises, and the join-table records that store reps/sets or duration for each exercise performed in a workout.

## Tech Stack
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite

## Installation

1. Clone the repository and enter the project:
   ```bash
   git clone <YOUR_GITHUB_REPO_URL>
   cd workout-api-summative
## Install dependencies:
pipenv install
pipenv shell
## Database Setup
Run migrations:
export FLASK_APP=server/app.py
flask db upgrade head

Seed the database (resets tables and inserts sample data):
cd server
python seed.py
cd ..
## Run the Server
cd server
python app.py

Server runs on:
http://127.0.0.1:5555
## API Endpoints
Workouts
GET /workouts
List all workouts
Includes associated workout_exercises with nested exercise data and reps/sets/duration
GET /workouts/<id>
Show a single workout including its associated workout_exercises
POST /workouts
Create a workout
Body example:
{
  "date": "2026-01-21",
  "duration_minutes": 45,
  "notes": "Upper body"
}
DELETE /workouts/<id>
Delete a workout (also deletes associated join records via cascade)
## Exercises
GET /exercises
List all exercises
GET /exercises/<id>
Show a single exercise and its associated workouts
POST /exercises
Create an exercise
Body example:
{
  "name": "Deadlift",
  "category": "Strength",
  "equipment_needed": true
}
DELETE /exercises/<id>
Delete an exercise (also deletes associated join records via cascade)
## Add Exercise to Workout (Join Table)
POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
Add an exercise to a workout with either:
sets + reps, OR
duration_seconds
Example (sets/reps):
{ "sets": 3, "reps": 10 }
Example (duration):
{ "duration_seconds": 90 }
## Validations
This API includes multiple layers of validation:
Database constraints (e.g., required fields, unique exercise name, positive numeric constraints)
Model validations using SQLAlchemy @validates
Marshmallow schema validations, including cross-field checks for join-table input
