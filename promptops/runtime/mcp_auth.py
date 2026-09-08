"""Owner-bound resource-server JWT verification using only a public RSA key."""
from pathlib import Path
from urllib.parse import urlsplit

from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
import jwt
from mcp.server.auth.provider import AccessToken


def https_url(value):
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("Authentication issuer and resource must be clean HTTPS URLs")
    return value


class OwnerTokenVerifier:
    def __init__(self, public_key_path, issuer, resource, subject):
        self.key = load_pem_public_key(Path(public_key_path).read_bytes())
        if not isinstance(self.key, RSAPublicKey) or self.key.key_size < 2048:
            raise ValueError("Use an RSA public key of at least 2048 bits")
        self.issuer = https_url(issuer)
        self.resource = https_url(resource)
        if not subject or len(subject) > 200:
            raise ValueError("An explicit owner subject is required")
        self.subject = subject

    async def verify_token(self, token):
        try:
            claims = jwt.decode(token, self.key, algorithms=["RS256"], audience=self.resource, issuer=self.issuer,
                                options={"require": ["exp", "iat", "sub", "aud", "iss"]})
            if claims["sub"] != self.subject or not isinstance(claims.get("scope"), str):
                return None
            scopes = claims["scope"].split()
            if "apastra:evaluate" not in scopes:
                return None
            return AccessToken(token=token, client_id=self.subject, scopes=scopes,
                               expires_at=claims["exp"], resource=self.resource)
        except (jwt.PyJWTError, TypeError, ValueError):
            return None
