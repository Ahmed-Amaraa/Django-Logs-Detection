import hmac
import hashlib

def calculate_signature(body, secret_key):
    return hmac.new(
        secret_key.encode(),
        body.encode(),
        hashlib.sha256
    ).hexdigest()