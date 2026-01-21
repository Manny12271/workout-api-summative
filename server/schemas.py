from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(
            min=2, error="name must be at least 2 characters")
    )
    category = fields.Str(
        required=True,
        validate=validate.Length(
            min=2, error="category must be at least 2 characters")
    )
    equipment_needed = fields.Bool(required=True)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)

    reps = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1, error="reps must be >= 1")
    )
    sets = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1, error="sets must be >= 1")
    )
    duration_seconds = fields.Int(
        allow_none=True,
        validate=validate.Range(min=1, error="duration_seconds must be >= 1")
    )

    workout_id = fields.Int(load_only=True)
    exercise_id = fields.Int(load_only=True)

    exercise = fields.Nested(ExerciseSchema, dump_only=True)

    @validates_schema
    def validate_rep_or_duration(self, data, **kwargs):
        reps = data.get("reps")
        sets = data.get("sets")
        duration = data.get("duration_seconds")

        if duration is None and (reps is None or sets is None):
            raise ValidationError(
                "Provide either duration_seconds OR both reps and sets.",
                field_name="workout_exercise"
            )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1, error="duration_minutes must be >= 1")
    )
    notes = fields.Str(allow_none=True)

    workout_exercises = fields.Nested(
        WorkoutExerciseSchema,
        many=True,
        dump_only=True
    )
