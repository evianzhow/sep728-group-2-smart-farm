import bcrypt
import secrets
from datetime import datetime, timezone

def hash_password(password: str) -> str:
    """
    Hash a plain-text password using bcrypt.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against a hashed password.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_session_token(username: str) -> str:
    """
    Generate a secure session token.
    """
    return secrets.token_hex(32)

def convert_datetime_to_iso8601(datetime_obj: datetime | str) -> str:
    """
    Convert a datetime object to an ISO 8601 string.
    """
    if type(datetime_obj) == str:
        datetime_obj = datetime.fromisoformat(datetime_obj.replace('Z', '+00:00'))
    elif type(datetime_obj) == datetime:
        pass
    else:
        raise ValueError("Invalid datetime object")
    # Ensure the datetime is in UTC (set timezone if needed)
    dt_utc = datetime_obj.replace(tzinfo=timezone.utc)

    # Format to the desired ISO 8601 format with 'Z' suffix
    formatted_time = dt_utc.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    return formatted_time

