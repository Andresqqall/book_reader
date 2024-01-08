from base64 import urlsafe_b64decode, urlsafe_b64encode
from django.core.signing import Signer

signer = Signer(sep=".")


def get_decoded_value(value):
    return signer.unsign(
        urlsafe_b64decode(
            value.encode('utf-8')
        ).decode('utf-8')
    )


def get_encoded_value(value):
    return urlsafe_b64encode(
        signer.sign(value).encode('utf-8')
    ).decode('utf-8')
