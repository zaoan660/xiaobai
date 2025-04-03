import jwt
from datetime import datetime, timezone, timedelta
from app.common.config import conf

ALGORITHM = "HS256"

def generate_jwt(user_id, token_ttl=7 * 24 * 60 * 60):
    exp = datetime.now(tz=timezone.utc) + timedelta(seconds=token_ttl)

    payload = {
        "user_id": user_id,
        # "ak_role": "user",
        "exp": exp,
    }
    token = jwt.encode(payload, conf.JWT_SECRET_KEY, algorithm=ALGORITHM)
    return token


