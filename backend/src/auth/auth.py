from fastapi import Security, HTTPException
from passlib.context import CryptContext
import jwt
from datetime import timedelta, datetime
import bcrypt
from fastapi.security import OAuth2PasswordBearer


class OAuth2Handler:
    _auth_bearer = OAuth2PasswordBearer(
        tokenUrl="/v1/admins/logins", scheme_name="access_token"
    )
    _password_context = CryptContext(schemes=["bcrypt"])
    _password_secret = "challenge-accepted"
    _token_secret = "challenge-accepted"
    _revoked_tokens = set()

    def get_password_hash(self, plain_password: str) -> str:
        encoded_password = plain_password.encode("utf-8")
        return bcrypt.hashpw(encoded_password, bcrypt.gensalt(12)).decode("utf-8")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        encoded_password = plain_password.encode("utf-8")
        encrypted_hash = hashed_password.encode("utf-8")
        return bcrypt.checkpw(encoded_password, encrypted_hash)

    def revoke_token(self, token):
        self._revoked_tokens.add(token)

    # encode token
    def create_token(self, admin_id: int) -> str:
        payload = {
            "exp": datetime.utcnow() + timedelta(hours=8),
            "iat": datetime.utcnow(),
            "admin_id": admin_id,
        }
        return jwt.encode(payload, self._token_secret, algorithm="HS256")

    # decode token
    def validate_token_and_get_admin_id(self, token) -> str:
        try:
            if token in self._revoked_tokens:
                raise HTTPException(status_code=401, detail="Token revoked")
            else:
                payload = jwt.decode(
                    jwt=token, key=self._token_secret, algorithms=["HS256"]
                )
                admin_id = payload["admin_id"]
            return admin_id
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Expired signature")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Token invalid")

    def auth_get_admin_id(self, token: str = Security(_auth_bearer)) -> str:
        return self.validate_token_and_get_admin_id(token)

    def auth_get_token(self, token: str = Security(_auth_bearer)) -> str:
        return token


auth_handler = OAuth2Handler()
