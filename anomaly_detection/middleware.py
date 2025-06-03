import hmac
import hashlib
from django.conf import settings
from django.http import HttpResponseForbidden

class HMACSignatureMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/') or request.path.startswith('/graphql/'):
            signature = request.headers.get(settings.HMAC_HEADER_NAME)
            if not signature:
                return HttpResponseForbidden('Missing HMAC signature')

            # Calculate expected signature
            body = request.body
            calculated_signature = hmac.new(
                settings.HMAC_SECRET_KEY.encode(),
                body,
                hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(signature, calculated_signature):
                return HttpResponseForbidden('Invalid HMAC signature')

        return self.get_response(request)