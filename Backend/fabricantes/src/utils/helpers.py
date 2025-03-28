from datetime import datetime
from uuid import UUID


def serialize_sqlalchemy(obj):
    if isinstance(obj, list):
        return [serialize_sqlalchemy(item) for item in obj]

    if not hasattr(obj, '__dict__'):
        return obj

    result = {}
    for key, value in obj.__dict__.items():
        if key.startswith("_"):
            # Skip private attributes
            continue
        if isinstance(value, datetime):
            # Convert datetime to string
            result[key] = value.isoformat()
        elif hasattr(value, '__dict__'):
            # Recursively serialize nested SQLAlchemy objects
            result[key] = serialize_sqlalchemy(value)
        else:
            result[key] = value
    return result


def is_valid_uuid(uuid):
    try:
        UUID(uuid)
    except ValueError:
        return False

    return True
